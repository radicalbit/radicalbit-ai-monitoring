from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
from utils.models import ModelOut, ModelType
from utils.reference_binary import ReferenceMetricsService
from utils.reference_multiclass import ReferenceMetricsMulticlassService
from utils.reference_regression import ReferenceMetricsRegressionService


class PercentageCalculator:
    @staticmethod
    def extract_drift_bool_values(drifts: list) -> list:
        """Feature is appended if there is at least one drift"""
        features_with_drift = []
        for feature_metric in drifts:
            feature_name = feature_metric['feature_name']
            drift_calc = feature_metric['drift_calc']
            if any(calc.get('has_drift', False) for calc in drift_calc):
                features_with_drift.append(feature_name)

        return features_with_drift

    @staticmethod
    def calculate_percentages(
        spark_session: SparkSession,
        drift,
        model_quality_current,
        current_dataset: CurrentDataset,
        reference_dataset: ReferenceDataset,
        prefix_id: str,
        model,
    ):
        # Compute percentage of drift
        feature_with_drifts = PercentageCalculator.extract_drift_bool_values(
            drift['feature_metrics']
        )
        perc_drift = {
            'value': 1 - (len(feature_with_drifts) / len(drift['feature_metrics'])),
            'details': [{'feature_name': x, 'score': 1.0} for x in feature_with_drifts],
        }

        # Compute percentage of model quality

        match model.model_type:
            case ModelType.BINARY:
                metrics_service = ReferenceMetricsService(
                    reference=reference_dataset, prefix_id=prefix_id
                )
            case ModelType.MULTI_CLASS:
                metrics_service = ReferenceMetricsMulticlassService(
                    reference=reference_dataset, prefix_id=prefix_id
                )
            case ModelType.REGRESSION:
                metrics_service = ReferenceMetricsRegressionService(
                    reference=reference_dataset, prefix_id=prefix_id
                )

        model_quality_reference = metrics_service.calculate_model_quality()

        def _compute_mq_percentage(metrics_cur, metric_ref):
            metrics_cur_np = np.array(metrics_cur)

            # bootstrap Parameters
            n_iterations = 500
            n_size = len(metrics_cur_np)

            # Use RandomState for better performance (avoid repeated seed calls)
            rng = np.random.RandomState(42)

            # Pre-allocate numpy array instead of list with append
            bootstrap_means = np.zeros(n_iterations)

            # perform bootstrap sampling
            for i in range(n_iterations):
                sample = rng.choice(metrics_cur_np, size=n_size, replace=True)
                bootstrap_means[i] = np.mean(sample)

            # calculate 95% confidence interval
            lower_bound = np.percentile(bootstrap_means, 2.5)
            upper_bound = np.percentile(bootstrap_means, 97.5)

            return 1 if not (lower_bound <= metric_ref <= upper_bound) else 0

        perc_model_quality = {'value': 0, 'details': []}
        if model.model_type in [ModelType.BINARY, ModelType.REGRESSION]:
            flagged_metrics = 0
            for key_m in model_quality_current['grouped_metrics']:
                metric_ref = model_quality_reference[key_m]
                metrics_cur = [
                    x['value'] for x in model_quality_current['grouped_metrics'][key_m]
                ]
                if len(metrics_cur) < 2:
                    # not enough values to do the test, return -1
                    perc_model_quality['value'] = -1
                    break
                is_flag = _compute_mq_percentage(metrics_cur, metric_ref)
                flagged_metrics += is_flag
                if is_flag:
                    perc_model_quality['details'].append(
                        {'feature_name': key_m, 'score': -1}
                    )
            perc_model_quality['value'] = 1 - (
                flagged_metrics / len(model_quality_current['grouped_metrics'])
            )

        elif model.model_type == ModelType.MULTI_CLASS:
            # Pre-build dictionary to avoid O(n²) nested loop
            class_metrics_map = {
                cm_ref['class_name']: cm_ref['metrics']
                for cm_ref in model_quality_reference['class_metrics']
            }

            flagged_metrics = 0
            cumulative_sum = 0
            for cm in model_quality_current['class_metrics']:
                current_class = cm['class_name']

                # Skip classes that don't exist in reference dataset
                if current_class not in class_metrics_map:
                    continue

                # O(1) lookup instead of nested loop
                mq_ref = class_metrics_map[current_class]

                for key_m in cm['grouped_metrics']:
                    metric_ref = mq_ref[key_m]
                    metrics_cur = [x['value'] for x in cm['grouped_metrics'][key_m]]
                    if len(metrics_cur) < 2:
                        # not enough values to do the test, return -1
                        cumulative_sum -= 10000
                    else:
                        is_flag = _compute_mq_percentage(metrics_cur, metric_ref)
                        flagged_metrics += is_flag
                        if is_flag:
                            perc_model_quality['details'].append(
                                {
                                    'feature_name': cm['class_name'] + '_' + key_m,
                                    'score': -1,
                                }
                            )
                cumulative_sum += 1 - (
                    flagged_metrics
                    / len(model_quality_reference['class_metrics'][0]['metrics'])
                )
                flagged_metrics = 0
            perc_model_quality['value'] = (
                cumulative_sum / len(model_quality_reference['classes'])
                if cumulative_sum > 0
                else -1
            )

        # Compute percentage of data quality
        def find_outliers(
            model: ModelOut,
            current_dataframe: DataFrame,
            reference_dataframe: DataFrame,
        ):
            # Cache DataFrames to avoid recomputation
            reference_dataframe.cache()
            current_dataframe.cache()

            try:
                # Switch between numerical and categorical columns
                numerical_features = [
                    numerical.name for numerical in model.get_numerical_features()
                ]

                categorical_features = [
                    categorical.name for categorical in model.get_categorical_features()
                ]
                details = []

                # Process numerical features with optimized approach
                if numerical_features:
                    # Build all outlier detection columns in one pass
                    outlier_columns = []

                    for column in numerical_features:
                        # Optimize: Single approxQuantile call for both Q1 and Q3
                        quantiles = reference_dataframe.approxQuantile(
                            column, [0.25, 0.75], relativeError=0
                        )
                        Q1, Q3 = quantiles[0], quantiles[1]

                        # IQR : Inter Quantile Range
                        IQR = Q3 - Q1

                        # selecting the data, with -1.5*IQR to + 1.5*IQR., where param = 1.5 default value
                        less_Q1 = Q1 - 1.5 * IQR
                        more_Q3 = Q3 + 1.5 * IQR

                        is_outlier_col = f'is_outlier_{column}'
                        outlier_columns.append(is_outlier_col)

                        current_dataframe = current_dataframe.withColumn(
                            is_outlier_col,
                            F.when(
                                (current_dataframe[column] > more_Q3)
                                | (current_dataframe[column] < less_Q1),
                                1,
                            ).otherwise(0),
                        )

                    # Optimize: Single aggregation for all numerical features
                    agg_exprs = [
                        F.sum(col).alias(f'sum_{col}') for col in outlier_columns
                    ]
                    agg_exprs.append(F.count('*').alias('total_count'))

                    results = current_dataframe.agg(*agg_exprs).collect()[0]
                    total_count = results['total_count']

                    for i, column in enumerate(numerical_features):
                        is_outlier_col = outlier_columns[i]
                        sum_value = results[f'sum_{is_outlier_col}']
                        score = sum_value / total_count if total_count > 0 else 0

                        details.append(
                            {
                                'feature_name': column,
                                'score': score,
                            }
                        )

                # Process categorical features
                if categorical_features:
                    # Optimize: Remove redundant .fit() - let pipeline do it
                    indexers = [
                        StringIndexer(
                            inputCol=column,
                            outputCol=column + '_index',
                            handleInvalid='keep',
                        )
                        for column in categorical_features
                    ]

                    pipeline = Pipeline(stages=indexers)
                    indexed_current_outliers_df = pipeline.fit(
                        reference_dataframe
                    ).transform(current_dataframe)

                    # Optimize: Pre-compute all distinct counts
                    distinct_counts = {}
                    for column in categorical_features:
                        distinct_counts[column] = (
                            reference_dataframe.select(column).distinct().count()
                        )

                    # Build outlier columns for categorical features
                    categorical_outlier_columns = []
                    cat_df = indexed_current_outliers_df
                    for column in categorical_features:
                        is_outlier_col = f'is_outlier_{column}'
                        categorical_outlier_columns.append(is_outlier_col)
                        count_reference = distinct_counts[column]

                        cat_df = cat_df.withColumn(
                            is_outlier_col,
                            F.when(
                                (
                                    indexed_current_outliers_df[column + '_index']
                                    > count_reference
                                ),
                                1,
                            ).otherwise(0),
                        )

                    # Optimize: Single aggregation for all categorical features
                    agg_exprs = [
                        F.sum(col).alias(f'sum_{col}')
                        for col in categorical_outlier_columns
                    ]
                    agg_exprs.append(F.count('*').alias('total_count'))

                    results = cat_df.agg(*agg_exprs).collect()[0]
                    total_count = results['total_count']

                    for i, column in enumerate(categorical_features):
                        is_outlier_col = categorical_outlier_columns[i]
                        sum_value = results[f'sum_{is_outlier_col}']
                        score = sum_value / total_count if total_count > 0 else 0

                        details.append(
                            {
                                'feature_name': column,
                                'score': score,
                            }
                        )

                return details

            finally:
                # Always unpersist cached DataFrames
                reference_dataframe.unpersist()
                current_dataframe.unpersist()

        det = find_outliers(model, current_dataset.current, reference_dataset.reference)

        # Optimize: Use sum() instead of loop
        s = sum(k['score'] for k in det) if det else 0

        perc_data_quality = {'value': 1 - (s / len(det)) if det else 1, 'details': det}

        return {
            'data_quality': perc_data_quality,
            'model_quality': perc_model_quality,
            'drift': perc_drift,
        }
