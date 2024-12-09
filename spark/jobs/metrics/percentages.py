from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from utils.models import ModelType
from utils.reference_binary import ReferenceMetricsService
from utils.reference_multiclass import ReferenceMetricsMulticlassService
from utils.reference_regression import ReferenceMetricsRegressionService
from pyspark.sql import DataFrame
from utils.models import ModelOut

import numpy as np


class PercentageCalculator:
    @staticmethod
    def calculate_percentages(
        spark_session: SparkSession,
        drift,
        model_quality_current,
        current_dataset: CurrentDataset,
        reference_dataset: ReferenceDataset,
        model,
    ):
        # Compute percentage of drift
        perc_drift = {
            "value": 1
            - (
                len(
                    [
                        x
                        for x in drift["feature_metrics"]
                        if x["drift_calc"]["has_drift"]
                    ]
                )
                / len(drift["feature_metrics"])
            ),
            "details": [
                {"feature_name": x["feature_name"], "score": 1.0}
                for x in drift["feature_metrics"]
                if x["drift_calc"]["has_drift"]
            ],
        }

        # Compute percentage of model quality

        match model.model_type:
            case ModelType.BINARY:
                metrics_service = ReferenceMetricsService(reference=reference_dataset)
            case ModelType.MULTI_CLASS:
                metrics_service = ReferenceMetricsMulticlassService(
                    reference=reference_dataset
                )
            case ModelType.REGRESSION:
                metrics_service = ReferenceMetricsRegressionService(
                    reference=reference_dataset
                )

        model_quality_reference = metrics_service.calculate_model_quality()

        def _compute_mq_percentage(metrics_cur, metric_ref):
            metrics_cur_np = np.array(metrics_cur)

            # bootstrap Parameters
            n_iterations = 500
            n_size = len(metrics_cur_np)
            bootstrap_means = []

            # perform bootstrap sampling
            np.random.seed(42)  # For reproducibility

            for _ in range(n_iterations):
                sample = np.random.choice(metrics_cur_np, size=n_size, replace=True)
                bootstrap_means.append(np.mean(sample))

            # calculate 95% confidence interval
            lower_bound = np.percentile(bootstrap_means, 2.5)
            upper_bound = np.percentile(bootstrap_means, 97.5)

            return 1 if not (lower_bound <= metric_ref <= upper_bound) else 0

        perc_model_quality = {"value": 0, "details": []}
        if model.model_type in [ModelType.BINARY, ModelType.REGRESSION]:
            flagged_metrics = 0
            for key_m in model_quality_current["grouped_metrics"]:
                metric_ref = model_quality_reference[key_m]
                metrics_cur = [
                    x["value"] for x in model_quality_current["grouped_metrics"][key_m]
                ]
                if len(metrics_cur) < 2:
                    # not enough values to do the test, return -1
                    perc_model_quality["value"] = -1
                    break
                else:
                    is_flag = _compute_mq_percentage(metrics_cur, metric_ref)
                    flagged_metrics += is_flag
                    if is_flag:
                        perc_model_quality["details"].append(
                            {"feature_name": key_m, "score": -1}
                        )
            perc_model_quality["value"] = 1 - (
                flagged_metrics / len(model_quality_current["grouped_metrics"])
            )

        elif model.model_type == ModelType.MULTI_CLASS:
            flagged_metrics = 0
            cumulative_sum = 0
            for cm in model_quality_current["class_metrics"]:
                for key_m in cm["grouped_metrics"]:
                    for cm_ref in model_quality_reference["class_metrics"]:
                        if cm_ref["class_name"] == cm["class_name"]:
                            mq_ref = cm_ref["metrics"]
                    metric_ref = mq_ref[key_m]
                    metrics_cur = [x["value"] for x in cm["grouped_metrics"][key_m]]
                    if len(metrics_cur) < 2:
                        # not enough values to do the test, return -1
                        cumulative_sum -= 10000
                    else:
                        is_flag = _compute_mq_percentage(metrics_cur, metric_ref)
                        flagged_metrics += is_flag
                        if is_flag:
                            perc_model_quality["details"].append(
                                {
                                    "feature_name": cm["class_name"] + "_" + key_m,
                                    "score": -1,
                                }
                            )
                cumulative_sum += 1 - (
                    flagged_metrics
                    / len(model_quality_reference["class_metrics"][0]["metrics"])
                )
                flagged_metrics = 0
            perc_model_quality["value"] = (
                cumulative_sum / len(model_quality_reference["classes"])
                if cumulative_sum > 0
                else -1
            )

        # Compute percentage of data quality
        def find_outliers(
            model: ModelOut,
            current_dataframe: DataFrame,
            reference_dataframe: DataFrame,
        ):
            # Switch between numerical and categorical columns
            numerical_features = [
                numerical.name for numerical in model.get_numerical_features()
            ]

            categorical_features = [
                categorical.name for categorical in model.get_categorical_features()
            ]
            details = []

            # Using the `for` loop to create new columns by identifying the outliers for each feature
            for column in numerical_features:
                # Q1 : First Quartile ., Q3 : Third Quartile
                Q1 = reference_dataframe.approxQuantile(column, [0.25], relativeError=0)
                Q3 = reference_dataframe.approxQuantile(column, [0.75], relativeError=0)

                # IQR : Inter Quantile Range
                # We need to define the index [0], as Q1 & Q3 are a set of lists., to perform a mathematical operation
                # Q1 & Q3 are defined separately so as to have a clear indication on First Quantile & 3rd Quantile
                IQR = Q3[0] - Q1[0]

                # selecting the data, with -1.5*IQR to + 1.5*IQR., where param = 1.5 default value
                less_Q1 = Q1[0] - 1.5 * IQR
                more_Q3 = Q3[0] + 1.5 * IQR

                is_outlier_col = "is_outlier_{}".format(column)

                current_dataframe = current_dataframe.withColumn(
                    is_outlier_col,
                    F.when(
                        (current_dataframe[column] > more_Q3)
                        | (current_dataframe[column] < less_Q1),
                        1,
                    ).otherwise(0),
                )

                details.append(
                    {
                        "feature_name": column,
                        "score": current_dataframe.select(is_outlier_col)
                        .groupby()
                        .sum()
                        .collect()[0][0]
                        / current_dataframe.select(is_outlier_col).count(),
                    }
                )

            indexers = [
                StringIndexer(
                    inputCol=column, outputCol=column + "_index", handleInvalid="keep"
                ).fit(reference_dataframe)
                for column in categorical_features
            ]

            pipeline = Pipeline(stages=indexers)
            indexed_current_outliers_df = pipeline.fit(reference_dataframe).transform(
                current_dataframe
            )

            for column in categorical_features:
                is_outlier_col = "is_outlier_{}".format(column)

                count_reference = reference_dataframe.select(column).distinct().count()

                current_dataframe = indexed_current_outliers_df.withColumn(
                    is_outlier_col,
                    F.when(
                        (
                            indexed_current_outliers_df[column + "_index"]
                            > count_reference
                        ),
                        1,
                    ).otherwise(0),
                )

                details.append(
                    {
                        "feature_name": column,
                        "score": current_dataframe.select(is_outlier_col)
                        .groupby()
                        .sum()
                        .collect()[0][0]
                        / current_dataframe.select(is_outlier_col).count(),
                    }
                )

            return details

        det = find_outliers(model, current_dataset.current, reference_dataset.reference)
        s = 0
        for k in det:
            s += k["score"]

        perc_data_quality = {"value": 1 - (s / len(det)), "details": det}

        return {
            "data_quality": perc_data_quality,
            "model_quality": perc_model_quality,
            "drift": perc_drift,
        }
