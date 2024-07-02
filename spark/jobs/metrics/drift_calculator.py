from pyspark.sql import SparkSession

from metrics.chi2 import Chi2Test
from metrics.ks import KolmogorovSmirnovTest
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset


class DriftCalculator:
    @staticmethod
    def calculate_drift(
        spark_session: SparkSession,
        reference_dataset: ReferenceDataset,
        current_dataset: CurrentDataset,
    ):
        drift_result = dict()
        drift_result["feature_metrics"] = []

        categorical_features = [
            categorical.name
            for categorical in reference_dataset.model.get_categorical_features()
        ]
        chi2 = Chi2Test(
            spark_session=spark_session,
            reference_data=reference_dataset.reference,
            current_data=current_dataset.current,
        )

        for column in categorical_features:
            feature_dict_to_append = {
                "feature_name": column,
                "drift_calc": {
                    "type": "CHI2",
                },
            }
            if (
                reference_dataset.reference_count > 5
                and current_dataset.current_count > 5
            ):
                result_tmp = chi2.test(column, column)
                feature_dict_to_append["drift_calc"]["value"] = float(
                    result_tmp["pValue"]
                )
                feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                    result_tmp["pValue"] <= 0.05
                )
            else:
                feature_dict_to_append["drift_calc"]["value"] = None
                feature_dict_to_append["drift_calc"]["has_drift"] = False
            drift_result["feature_metrics"].append(feature_dict_to_append)

        numerical_features = [
            numerical.name
            for numerical in reference_dataset.model.get_numerical_features()
        ]
        ks = KolmogorovSmirnovTest(
            reference_data=reference_dataset.reference,
            current_data=current_dataset.current,
            alpha=0.05,
            phi=0.004,
        )

        for column in numerical_features:
            feature_dict_to_append = {
                "feature_name": column,
                "drift_calc": {
                    "type": "KS",
                },
            }
            result_tmp = ks.test(column, column)
            feature_dict_to_append["drift_calc"]["value"] = float(
                result_tmp["ks_statistic"]
            )
            feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                result_tmp["ks_statistic"] > result_tmp["critical_value"]
            )
            drift_result["feature_metrics"].append(feature_dict_to_append)

        return drift_result
