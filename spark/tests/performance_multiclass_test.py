"""Performance test to demonstrate the nested loop catastrophe issue.

Run with: pytest tests/performance_multiclass_test.py -v -s

This test generates a large dataset with many time groups to showcase
the performance difference between original and optimized code.
"""

import datetime
import random
import uuid

from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from pyspark.sql import Row
import pytest
from utils.current_multiclass import CurrentMetricsMulticlassService

from jobs.utils.models import (
    ColumnDefinition,
    DataType,
    FieldTypes,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)
from tests.utils.pytest_utils import prefix_id


@pytest.fixture
def large_dataset_for_performance(spark_fixture):
    """Generate a large dataset with:
    - 10,000 rows
    - 5 classes
    - 100 time groups (hourly over ~4 days)
    - 4 features

    This will trigger: 5 classes × 5 metrics × 100 time groups = 2,500 evaluations
    """
    random.seed(42)

    classes = ['CLASS_A', 'CLASS_B', 'CLASS_C', 'CLASS_D', 'CLASS_E']
    cat1_values = ['X', 'Y', 'Z']
    cat2_values = ['P', 'Q', 'R']

    # Base datetime
    base_dt = datetime.datetime(2024, 6, 1, 0, 0, 0)

    # Generate reference data (small, just needs one row per class)
    reference_data = []
    for i, cls in enumerate(classes):
        reference_data.append(
            Row(
                cat1=random.choice(cat1_values),
                cat2=random.choice(cat2_values),
                num1=round(random.uniform(0.0, 100.0), 2),
                num2=round(random.uniform(0.0, 500.0), 2),
                prediction=cls,
                target=cls,
                datetime=str(base_dt + datetime.timedelta(hours=i)),
            )
        )

    # Generate current data (10,000 rows across 100 hours)
    current_data = []
    rows_per_hour = 100
    num_hours = 100

    for hour in range(num_hours):
        dt = base_dt + datetime.timedelta(hours=hour)
        for _ in range(rows_per_hour):
            true_class = random.choice(classes)
            # 80% accuracy
            pred_class = true_class if random.random() < 0.8 else random.choice(classes)

            current_data.append(
                Row(
                    cat1=random.choice(cat1_values),
                    cat2=random.choice(cat2_values),
                    num1=round(random.uniform(0.0, 100.0), 2),
                    num2=round(random.uniform(0.0, 500.0), 2),
                    prediction=pred_class,
                    target=true_class,
                    datetime=str(
                        dt + datetime.timedelta(minutes=random.randint(0, 59))
                    ),
                )
            )

    reference_df = spark_fixture.createDataFrame(reference_data)
    current_df = spark_fixture.createDataFrame(current_data)

    return reference_df, current_df


def test_performance_large_dataset(spark_fixture, large_dataset_for_performance):
    """Performance test with a large dataset.

    Expected behavior:
    - ORIGINAL CODE: Very slow due to nested loop triggering ~2,500 Spark jobs
    - OPTIMIZED CODE: Much faster with caching and batched computation
    """
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.string, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='performance_test_model',
        description='Performance test for multiclass metrics',
        model_type=ModelType.MULTI_CLASS,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    reference_dataframe, current_dataframe = large_dataset_for_performance
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=current_dataframe, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_dataframe, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality()

    # Basic validation
    assert model_quality is not None
    assert 'classes' in model_quality
    assert 'class_metrics' in model_quality
    assert 'global_metrics' in model_quality
    assert len(model_quality['classes']) == 5
