from pyspark.sql import SparkSession

from metrics.chi2 import Chi2Test
from metrics.ks import KolmogorovSmirnovTest
from metrics.psi import PSI
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
                result_tmp = chi2.test_goodness_fit(column, column)
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

        float_features = [
            float_f.name for float_f in reference_dataset.model.get_float_features()
        ]
        ks = KolmogorovSmirnovTest(
            reference_data=reference_dataset.reference,
            current_data=current_dataset.current,
            alpha=0.05,
            phi=0.004,
        )

        for column in float_features:
            feature_dict_to_append = {
                "feature_name": column,
                "drift_calc": {},
            }
            unique_values_ref = (
                reference_dataset.reference.select(column)
                .distinct()
                .rdd.flatMap(lambda x: x)
                .collect()
            )
            unique_values_cur = (
                current_dataset.current.select(column)
                .distinct()
                .rdd.flatMap(lambda x: x)
                .collect()
            )
            unique_values_refcur = unique_values_ref + unique_values_cur
            lookup = set()
            unique_values_tot = [
                x
                for x in unique_values_refcur
                if x is not None and x not in lookup and lookup.add(x) is None
            ]
            if len(unique_values_tot) < 15:
                feature_dict_to_append["drift_calc"]["type"] = "CHI2"
                if (
                    reference_dataset.reference_count > 5
                    and current_dataset.current_count > 5
                ):
                    result_tmp = chi2.test_goodness_fit(column, column)
                    feature_dict_to_append["drift_calc"]["value"] = float(
                        result_tmp["pValue"]
                    )
                    feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                        result_tmp["pValue"] <= 0.05
                    )
                else:
                    feature_dict_to_append["drift_calc"]["value"] = None
                    feature_dict_to_append["drift_calc"]["has_drift"] = False
            else:
                feature_dict_to_append["drift_calc"]["type"] = "KS"
                result_tmp = ks.test(column, column)
                feature_dict_to_append["drift_calc"]["value"] = float(
                    result_tmp["ks_statistic"]
                )
                feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                    result_tmp["ks_statistic"] > result_tmp["critical_value"]
                )
            drift_result["feature_metrics"].append(feature_dict_to_append)

        int_features = [
            int_f.name for int_f in reference_dataset.model.get_int_features()
        ]
        psi_obj = PSI(
            spark_session=spark_session,
            reference_data=reference_dataset.reference,
            current_data=current_dataset.current,
        )
        for column in int_features:
            feature_dict_to_append = {
                "feature_name": column,
                "drift_calc": {},
            }
            unique_values_ref = (
                reference_dataset.reference.select(column)
                .distinct()
                .rdd.flatMap(lambda x: x)
                .collect()
            )
            unique_values_cur = (
                current_dataset.current.select(column)
                .distinct()
                .rdd.flatMap(lambda x: x)
                .collect()
            )
            unique_values_refcur = unique_values_ref + unique_values_cur
            lookup = set()
            unique_values_tot = [
                x
                for x in unique_values_refcur
                if x is not None and x not in lookup and lookup.add(x) is None
            ]
            if len(unique_values_tot) < 15:
                feature_dict_to_append["drift_calc"]["type"] = "CHI2"
                if (
                    reference_dataset.reference_count > 5
                    and current_dataset.current_count > 5
                ):
                    result_tmp = chi2.test_goodness_fit(column, column)
                    feature_dict_to_append["drift_calc"]["value"] = float(
                        result_tmp["pValue"]
                    )
                    feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                        result_tmp["pValue"] <= 0.05
                    )
                else:
                    feature_dict_to_append["drift_calc"]["value"] = None
                    feature_dict_to_append["drift_calc"]["has_drift"] = False
            else:
                feature_dict_to_append["drift_calc"]["type"] = "PSI"
                result_tmp = psi_obj.calculate_psi(column)
                feature_dict_to_append["drift_calc"]["value"] = float(
                    result_tmp["psi_value"]
                )
                feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                    result_tmp["psi_value"] >= 0.2
                )
            drift_result["feature_metrics"].append(feature_dict_to_append)

        return drift_result
