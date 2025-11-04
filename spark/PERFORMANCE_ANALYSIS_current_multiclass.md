# Spark Performance Analysis: current_multiclass.py

## Critical Performance Issues

### 1. ❌ Excessive Driver Memory Usage via `.collect()` Operations
**Location:** Lines 128-134, 182 (in CurrentDataset.get_string_indexed_dataframe)

**Issue:**
```python
list_of_time_group = (
    dataset_with_group.select('time_group')
    .distinct()
    .orderBy(F.col('time_group').asc())
    .rdd.flatMap(lambda x: x)
    .collect()  # ⚠️ Brings all time groups to driver
)
```

**Performance Penalty:**
- **Driver OOM Risk**: All distinct time groups loaded into driver memory
- **Network Transfer**: Full dataset scan + distinct operation + data transfer to driver
- **Memory Usage**: O(n) where n = number of distinct time groups
- **Impact**: High for datasets with many time periods (hourly granularity over months = thousands of groups)

---

### 2. ❌ N+1 Query Pattern with Lazy DataFrame Filtering
**Location:** Lines 135-138

**Issue:**
```python
array_of_groups = [
    dataset_with_group.where(F.col('time_group') == x)
    for x in list_of_time_group
]
```

**Performance Penalty:**
- **Problem**: Creates N lazy DataFrames, each will scan the full dataset when executed
- **Execution Count**: Each filtered DataFrame is evaluated 5 times (once per metric) in nested loops
- **No Partitioning**: Filters applied without leveraging Spark partitioning strategies
- **Impact**: O(n × m) full table scans where n = time groups, m = metrics per class

---

### 3. ❌ Catastrophic Nested Loop with Repeated Spark Job Execution
**Location:** Lines 140-168

**Issue:**
```python
return [
    {
        'class_name': label,
        'metrics': {
            metric_label: self.__evaluate_multi_class_classification(
                self.indexed_current, metric_name, float(index)
            )  # ⚠️ Executed C × M times on full dataset
            for (metric_name, metric_label) in ...
        },
        'grouped_metrics': {
            metric_label: [
                {
                    'timestamp': group,
                    'value': self.__evaluate_multi_class_classification(
                        group_dataset, metric_name, float(index)
                    ),  # ⚠️ Executed C × M × T times on filtered datasets
                }
                for group, group_dataset in zip(list_of_time_group, array_of_groups)
            ]
            for metric_name, metric_label in ...
        },
    }
    for index, label in self.index_label_map.items()
]
```

**Performance Penalty:**
- **Job Explosion**: 
  - Global metrics: C × M evaluations (e.g., 3 classes × 5 metrics = 15 jobs)
  - Time-grouped metrics: C × M × T evaluations (e.g., 3 × 5 × 100 = 1,500 jobs)
  - **Total**: Can trigger 1,500+ Spark jobs for a single analysis!
- **Scheduling Overhead**: Each job has submission, planning, and scheduling latency (~100-500ms per job)
- **Redundant Computation**: Same dataset scanned repeatedly for different metrics
- **Cluster Underutilization**: Jobs submitted sequentially due to nested comprehensions
- **Wall Time**: Linear scaling with number of jobs (hours for large datasets with many time periods)

**Example Calculation:**
- 10 classes × 5 metrics × 200 time groups = **10,000 separate Spark jobs**
- At 200ms avg per job = **33+ minutes just in job overhead**

---

### 4. ❌ No DataFrame Caching for Frequently Reused Data
**Location:** Throughout the class

**Issue:**
- `self.indexed_current` - used in multiple methods, never cached
- `dataset_with_group` - filtered N times, never cached
- Each element in `array_of_groups` - evaluated 5 times (once per metric)

**Performance Penalty:**
- **Recomputation**: Same transformations re-executed multiple times
- **I/O Overhead**: Re-reading from source for each computation
- **Memory Waste**: No reuse of already computed data
- **Impact**: 5-10x slowdown when the same DataFrame is used repeatedly

**Missing `.cache()` calls:**
```python
# Should be:
self.indexed_current.cache()
dataset_with_group.cache()
for df in array_of_groups:
    df.cache()
```

---

### 5. ❌ Expensive Nested Date Formatting Operations
**Location:** Lines 90-106 (WEEK granularity), 116-124 (other granularities)

**Issue:**
```python
F.date_format(
    F.to_timestamp(
        F.date_sub(
            F.next_day(
                F.date_format(
                    self.current.model.timestamp.name,
                    create_time_format(self.current.model.granularity)
                ),
                'sunday',
            ),
            7,
        )
    ),
    'yyyy-MM-dd HH:mm:ss',
).alias('time_group')
```

**Performance Penalty:**
- **CPU-Intensive**: 5-6 nested function calls per row
- **String Operations**: Multiple string parsing/formatting operations
- **Non-Vectorized**: Applied row-by-row rather than vectorized operations
- **Impact**: 2-3x slower than simplified date truncation
- **Better Alternative**: Use `F.date_trunc()` or pre-computed columns

---

### 6. ❌ Inefficient Confusion Matrix Calculation
**Location:** Lines 194-202

**Issue:**
```python
def __calc_confusion_matrix(self):
    prediction_and_labels = self.indexed_current.select(
        *[
            f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx',
            f'{self.prefix_id}_{self.reference.model.target.name}-idx',
        ]
    ).rdd  # ⚠️ Convert to RDD
    multiclass_metrics_calculator = MulticlassMetrics(prediction_and_labels)
    return multiclass_metrics_calculator.confusionMatrix().toArray().tolist()  # ⚠️ Collect to driver
```

**Performance Penalty:**
- **DataFrame → RDD Conversion**: Loses Catalyst optimizer benefits
- **Full Data Collection**: Confusion matrix materialized on driver
- **Memory Risk**: For large datasets with many classes, matrix size = C² × 8 bytes
- **Impact**: 
  - 100 classes = 10,000 cells = ~80KB (acceptable)
  - 1,000 classes = 1,000,000 cells = ~8MB (marginal)
  - But the full dataset scan through RDD is inefficient

---

### 7. ❌ Cartesian Product via Dummy Window Partition
**Location:** CurrentDataset.get_string_indexed_dataframe (lines 142-149)

**Issue:**
```python
classes_index_df = (
    prediction_target_df.select(f'{self.prefix_id}_classes')
    .distinct()
    .withColumn(
        f'{self.prefix_id}_classes_index',
        (
            F.row_number().over(
                Window.partitionBy(F.lit('A')).orderBy(f'{self.prefix_id}_classes')
            )  # ⚠️ Single partition - no parallelism!
            - 1
        ).cast(DoubleType()),
    )
)
```

**Performance Penalty:**
- **Single Partition**: `Window.partitionBy(F.lit('A'))` forces all data into one partition
- **No Parallelism**: Window function executed sequentially on single executor
- **Unnecessary Shuffle**: All distinct classes shuffled to a single partition
- **Impact**: O(n) sequential operation where n = number of distinct classes
- **Alternative**: Use `F.monotonically_increasing_id()` or `zipWithIndex()` on RDD

---

### 8. ❌ Multiple Sequential Joins Without Broadcast Optimization
**Location:** CurrentDataset.get_string_indexed_dataframe (lines 152-176)

**Issue:**
```python
indexed_prediction_df = (
    self.current.join(
        classes_index_df,  # Small table, should be broadcast
        self.current[self.model.outputs.prediction.name]
        == classes_index_df[f'{self.prefix_id}_classes'],
        how='inner',
    )
    # ... then another join
)
indexed_target_df = (
    indexed_prediction_df.join(
        classes_index_df,  # Same small table joined again
        indexed_prediction_df[self.model.target.name]
        == classes_index_df[f'{self.prefix_id}_classes'],
        how='inner',
    )
)
```

**Performance Penalty:**
- **Two Sort-Merge Joins**: Without broadcast hints, Spark uses expensive sort-merge joins
- **Data Shuffling**: Both joins require shuffling large datasets
- **Redundant Shuffle**: Second join shuffles already-shuffled data
- **Impact**: 2 × shuffle overhead when broadcast join would be O(1) network transfer
- **Better**: `F.broadcast(classes_index_df)` for both joins

---

## Performance Impact Summary

| Issue | Severity | Time Impact | Memory Impact |
|-------|----------|-------------|---------------|
| Nested loop evaluations | 🔴 Critical | 10-100x | Low |
| No caching | 🔴 Critical | 5-10x | High (wasted recomputation) |
| Multiple .collect() | 🟠 High | 2-5x | High (driver OOM risk) |
| N+1 query pattern | 🟠 High | 5-20x | Medium |
| Nested date formatting | 🟡 Medium | 2-3x | Low |
| Window with single partition | 🟡 Medium | 2-5x | Medium |
| Sequential joins | 🟡 Medium | 2-3x | High (shuffle) |
| RDD conversion | 🟢 Low | 1.5-2x | Low |

---

## Recommended Optimization Strategy

1. **Immediate Priority**: Add `.cache()` to `self.indexed_current` and time-grouped DataFrames
2. **High Priority**: Replace nested loop with single batch computation using window functions
3. **High Priority**: Use broadcast joins for small lookup tables
4. **Medium Priority**: Simplify date formatting to use `F.date_trunc()` or window-based time bucketing
5. **Medium Priority**: Replace dummy window partition with proper indexing strategy
6. **Low Priority**: Consider keeping confusion matrix computation as-is unless class count > 1000

## Estimated Performance Gain
With all optimizations: **20-50x speedup** for typical workloads (3-10 classes, 50-200 time groups)