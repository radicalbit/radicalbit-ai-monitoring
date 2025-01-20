from typing import List, Optional

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from metrics.data_quality_calculator import DataQualityCalculator
from models.current_dataset import CurrentDataset
from models.data_quality import (
    CategoricalFeatureMetrics,
    NumericalFeatureMetrics,
    NumericalTargetMetrics,
    RegressionDataQuality,
)
from models.reference_dataset import ReferenceDataset
from models.regression_model_quality import ModelQualityRegression, RegressionMetricType
from metrics.model_quality_regression_calculator import ModelQualityRegressionCalculator
from .misc import create_time_format
from .models import Granularity
from metrics.drift_calculator import DriftCalculator


class CurrentMetricsRegressionService:
    def __init__(
        self,
        spark_session: SparkSession,
        current: CurrentDataset,
        reference: ReferenceDataset,
        prefix_id: str,
    ):
        self.spark_session = spark_session
        self.current = current
        self.reference = reference
        self.prefix_id = prefix_id

    def calculate_model_quality(self) -> ModelQualityRegression:
        metrics = dict()
        metrics["global_metrics"] = ModelQualityRegressionCalculator.numerical_metrics(
            model=self.current.model,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
            prefix_id=self.prefix_id,
        ).model_dump(serialize_as_any=True)
        metrics["grouped_metrics"] = (
            self.calculate_regression_model_quality_group_by_timestamp()
        )
        metrics["global_metrics"]["residuals"] = (
            ModelQualityRegressionCalculator.residual_metrics(
                model=self.current.model,
                dataframe=self.current.current,
                prefix_id=self.prefix_id,
            )
        )
        return metrics

    def calculate_regression_model_quality_group_by_timestamp(self):
        if self.current.model.granularity == Granularity.WEEK:
            dataset_with_group = self.current.current.select(
                [
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    F.date_format(
                        F.to_timestamp(
                            F.date_sub(
                                F.next_day(
                                    F.date_format(
                                        self.current.model.timestamp.name,
                                        create_time_format(
                                            self.current.model.granularity
                                        ),
                                    ),
                                    "sunday",
                                ),
                                7,
                            )
                        ),
                        "yyyy-MM-dd HH:mm:ss",
                    ).alias("time_group"),
                ]
            )
        else:
            dataset_with_group = self.current.current.select(
                [
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    F.date_format(
                        F.to_timestamp(
                            F.date_format(
                                self.current.model.timestamp.name,
                                create_time_format(self.current.model.granularity),
                            )
                        ),
                        "yyyy-MM-dd HH:mm:ss",
                    ).alias("time_group"),
                ]
            )

        list_of_time_group = (
            dataset_with_group.select("time_group")
            .distinct()
            .orderBy(F.col("time_group").asc())
            .rdd.flatMap(lambda x: x)
            .collect()
        )
        array_of_groups = [
            dataset_with_group.where(F.col("time_group") == x)
            for x in list_of_time_group
        ]

        return {
            metric_name.value: [
                {
                    "timestamp": group,
                    "value": ModelQualityRegressionCalculator.eval_model_quality_metric(
                        self.current.model,
                        group_dataset,
                        group_dataset.count(),
                        metric_name,
                        self.prefix_id,
                    ),
                }
                for group, group_dataset in zip(list_of_time_group, array_of_groups)
            ]
            for metric_name in RegressionMetricType
        }

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        return DataQualityCalculator.calculate_combined_data_quality_numerical(
            model=self.current.model,
            current_dataframe=self.current.current,
            current_count=self.current.current_count,
            reference_dataframe=self.reference.reference,
            spark_session=self.spark_session,
            prefix_id=self.prefix_id,
        )

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        return DataQualityCalculator.categorical_metrics(
            model=self.current.model,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
            prefix_id=self.prefix_id,
        )

    def calculate_target_metrics(self) -> NumericalTargetMetrics:
        return DataQualityCalculator.regression_target_metrics(
            target_column=self.current.model.target.name,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
        )

    def calculate_current_target_metrics(self) -> NumericalTargetMetrics:
        return DataQualityCalculator.regression_target_metrics_current(
            target_column=self.current.model.target.name,
            curr_df=self.current.current,
            curr_count=self.current.current_count,
            ref_df=self.reference.reference,
            spark_session=self.spark_session,
            prefix_id=self.prefix_id,
        )

    def calculate_data_quality(
        self, is_current: Optional[bool] = False
    ) -> RegressionDataQuality:
        feature_metrics = []
        if self.reference.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.reference.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        target_metrics = (
            self.calculate_target_metrics()
            if not is_current
            else self.calculate_current_target_metrics()
        )
        return RegressionDataQuality(
            n_observations=self.current.current_count,
            target_metrics=target_metrics,
            feature_metrics=feature_metrics,
        )

    def calculate_drift(self):
        return DriftCalculator.calculate_drift(
            spark_session=self.spark_session,
            reference_dataset=self.reference,
            current_dataset=self.current,
            prefix_id=self.prefix_id,
        )
