import math
from math import ceil, sqrt

import numpy as np
from numpy import interp, linspace
from pyspark.sql import DataFrame, SparkSession
from utils.drift_detector import DriftDetector
from utils.models import ColumnDefinition, DriftAlgorithmType, FieldTypes


class KolmogorovSmirnovTest(DriftDetector):
    """Implement the Kolmogorov-Smirnov test as described in the paper: https://arxiv.org/pdf/2312.09380.
    It is designed to compare two sample distributions and determine if they differ significantly.
    """

    def __init__(
        self,
        spark_session: SparkSession,
        reference_data: DataFrame,
        current_data: DataFrame,
        prefix_id: str,
        phi: float = 0.004,
    ) -> None:
        """Initialize the KolmogorovSmirnovTest with the provided data and parameters.

        Parameters:
        - spark_session (SparkSession): SparkSession
        - reference_data (DataFrame): The reference data as a Spark DataFrame.
        - current_data (DataFrame): The current data as a Spark DataFrame.
        - p_value (float): The significance level for the hypothesis test.
        - phi (float): ϕ defines the precision of the KS test statistic.

        """
        self.spark_session = spark_session
        self.prefix_id = prefix_id
        self.reference_data = reference_data
        self.current_data = current_data
        self.phi = phi
        self.reference_size = self.reference_data.count()
        self.current_size = self.current_data.count()

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.numerical]

    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs['p_value']:
            raise AttributeError('p_value is not defined in kwargs')
        p_value = self.__critical_value(significance_level=kwargs['p_value'])
        feature_dict_to_append['type'] = DriftAlgorithmType.KS
        feature_dict_to_append['limit'] = float(p_value)
        result_tmp = self.test(feature.name, feature.name)
        if result_tmp['ks_statistic'] is None or math.isnan(result_tmp['ks_statistic']):
            feature_dict_to_append['value'] = -1
            feature_dict_to_append['has_drift'] = False
            return feature_dict_to_append
        feature_dict_to_append['value'] = float(result_tmp['ks_statistic'])
        feature_dict_to_append['has_drift'] = bool(result_tmp['ks_statistic'] > p_value)
        return feature_dict_to_append

    @staticmethod
    def __eps45(n, delta) -> float:
        """Select value of epsilon at the elbow of unit slope.
        Return 0, for no approximation if delta < 0
        """

        return max(0.0, delta - sqrt(delta / n))

    @staticmethod
    def __num_probs(n, delta: float, epsilon: float) -> int:
        """Calculate number of probability points for approx
        quantiles; at most this is the number of data points.

        Returns:
            - int: the number of probability points

        """

        a = 1 / (delta - epsilon) + 1
        return min(ceil(a), n)

    def __critical_value(self, significance_level) -> float:
        """Compute the critical value for the KS test at a given alpha level.

        Returns:
            - float: the critical value for a given alpha

        """

        return np.sqrt(-0.5 * np.log(significance_level / 2)) * np.sqrt(
            (self.reference_size + self.current_size)
            / (self.reference_size * self.current_size)
        )

    def test(self, reference_column: str, current_column: str) -> dict:
        """Approximates two-sample KS distance with precision
        phi between columns of Spark DataFrames.

        Parameters:
        - reference_column (str): The column name in the reference data.
        - current_column (str): The column name in the current data.

        """

        delta = self.phi / 2

        eps45x = self.__eps45(delta=delta, n=self.reference_size)
        eps45y = self.__eps45(delta=delta, n=self.current_size)

        ax = self.__num_probs(n=self.reference_size, delta=delta, epsilon=eps45x)
        ay = self.__num_probs(n=self.current_size, delta=delta, epsilon=eps45y)

        pxi = linspace(1 / self.reference_size, 1, ax)
        pyj = linspace(1 / self.current_size, 1, ay)

        xi = self.reference_data.approxQuantile(reference_column, list(pxi), eps45x)
        yj = self.current_data.approxQuantile(current_column, list(pyj), eps45y)

        f_xi = pxi
        f_yi = interp(xi, yj, pyj)

        f_yj = pyj
        f_xj = interp(yj, xi, pxi)

        d_i = max(abs(f_xi - f_yi))
        d_j = max(abs(f_xj - f_yj))
        d_ks = max(d_i, d_j)

        return {
            'ks_statistic': round(d_ks, 10),
        }
