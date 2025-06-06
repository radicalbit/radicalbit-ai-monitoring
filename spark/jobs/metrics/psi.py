import math
from math import inf

import numpy as np
from pyspark.ml.feature import Bucketizer
from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from utils.drift_detector import DriftDetector
from utils.models import ColumnDefinition, DriftAlgorithmType, FieldTypes


class PSI(DriftDetector):
    """Implement the PSI (population stability index).
    It is designed to compare two sample distributions and determine if they differ significantly.
    """

    def __init__(
        self,
        spark_session: SparkSession,
        reference_data: DataFrame,
        current_data: DataFrame,
        prefix_id: str,
    ) -> None:
        """Initialize the Population Stability Index with the provided data and parameters.

        Parameters:
        - spark_session(SparkSession): The SparkSession object.
        - reference_data (DataFrame): The reference data as a Spark DataFrame.
        - current_data (DataFrame): The current data as a Spark DataFrame.

        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.prefix_id = prefix_id

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.numerical]

    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs['threshold']:
            raise AttributeError('threshold is not defined in kwargs')
        threshold = kwargs['threshold']
        feature_dict_to_append['type'] = DriftAlgorithmType.PSI
        feature_dict_to_append['limit'] = threshold
        result_tmp = self.calculate_psi(feature.name)
        if result_tmp['psi_value'] is None or math.isnan(result_tmp['psi_value']):
            feature_dict_to_append['value'] = -1
            feature_dict_to_append['has_drift'] = False
            return feature_dict_to_append
        feature_dict_to_append['value'] = float(result_tmp['psi_value'])
        feature_dict_to_append['has_drift'] = bool(result_tmp['psi_value'] > threshold)
        return feature_dict_to_append

    @staticmethod
    def sub_psi(e_perc, a_perc):
        """Calculate the actual PSI value from comparing the values.
        Update the actual value to a very small number if equal to zero
        """
        if a_perc == 0:
            a_perc = 0.0001
        if e_perc == 0:
            e_perc = 0.0001

        return (e_perc - a_perc) * np.log(e_perc / a_perc)

    def calculate_psi(self, feature) -> dict:
        # first compute bucket as a list from 0 to 10 (or distinct().count() of the values in columns)

        current = self.current_data.withColumn(
            f'{self.prefix_id}_type', F.lit('current')
        )
        reference = self.reference_data.withColumn(
            f'{self.prefix_id}_type', F.lit('reference')
        )

        reference_and_current = (
            current.select([feature, f'{self.prefix_id}_type'])
            .unionByName(reference.select([feature, f'{self.prefix_id}_type']))
            .dropna()
        )

        max_value = reference_and_current.agg(
            F.max(
                F.when(
                    F.col(feature).isNotNull() & ~F.isnan(feature),
                    F.col(feature),
                )
            )
        ).collect()[0][0]
        min_value = reference_and_current.agg(
            F.min(
                F.when(
                    F.col(feature).isNotNull() & ~F.isnan(feature),
                    F.col(feature),
                )
            )
        ).collect()[0][0]

        distinct_features = (
            reference_and_current.select(feature).distinct().orderBy(feature)
        )
        dist_cnt = distinct_features.count()
        if dist_cnt < 10:
            buckets_spacing = distinct_features.rdd.flatMap(lambda x: x).collect()
            buckets_spacing.append(buckets_spacing[-1] + 1)
        else:
            buckets_spacing = np.linspace(min_value, max_value, 11).tolist()

        lookup = set()
        generated_buckets = [
            x for x in buckets_spacing if x not in lookup and lookup.add(x) is None
        ]
        # workaround if all values are the same to not have errors
        if len(generated_buckets) == 1:
            # buckets_spacing = [generated_buckets[0], generated_buckets[0]]
            buckets = [-float(inf), generated_buckets[0], float(inf)]
        else:
            buckets = generated_buckets

        bucketizer = Bucketizer(splits=buckets, inputCol=feature, outputCol='bucket')
        result = bucketizer.setHandleInvalid('keep').transform(reference_and_current)

        current_df = (
            result.filter(F.col(f'{self.prefix_id}_type') == 'current')
            .groupBy('bucket')
            .agg(F.count(F.col(feature)).alias('curr_count'))
        )
        reference_df = (
            result.filter(F.col(f'{self.prefix_id}_type') == 'reference')
            .groupBy('bucket')
            .agg(F.count(F.col(feature)).alias('ref_count'))
        )

        buckets_number = list(range(10))
        bucket_df = self.spark_session.createDataFrame(
            buckets_number, IntegerType()
        ).withColumnRenamed('value', 'bucket')
        tot_df = (
            bucket_df.join(current_df, on=['bucket'], how='left')
            .join(reference_df, on=['bucket'], how='left')
            .fillna(0)
            .orderBy('bucket')
        )
        # workaround if all values are the same to not have errors
        if len(generated_buckets) == 1:
            tot_df = tot_df.filter(F.col('bucket') == 1)
        current_hist = tot_df.select('curr_count').rdd.flatMap(lambda x: x).collect()
        reference_hist = tot_df.select('ref_count').rdd.flatMap(lambda x: x).collect()
        current_fractions = [x / sum(current_hist) for x in current_hist]
        reference_fractions = [x / sum(reference_hist) for x in reference_hist]

        # compute PSI for each bucket and sum
        psi_value = sum(
            PSI.sub_psi(reference_fractions[i], current_fractions[i])
            for i in range(len(reference_fractions))
        )

        return {'psi_value': float(psi_value)}
