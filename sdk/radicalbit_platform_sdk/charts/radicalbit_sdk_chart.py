from typing import List

from ipecharts import EChartsRawWidget
import ipywidgets as widgets

from .binary_classification.binary_chart import (
    BinaryChart,
    BinaryDistributionChartData,
)

from .common.chart import Chart
from .common.chart_data import (
    ConfusionMatrixChartData,
    LinearChartData,
    NumericalBarChartData,
)
from .multi_classification.multi_class_chart import (
    MultiClassificationChart,
    MultiClassificationDistributionChartData,
)
from .multi_classification.multi_class_chart_data import (
    MultiClassificationLinearChartData,
)
from .radicalbit_sdk_chart_data import (
    RbitChartData,
    RbitChartLinearData,
    RbitChartResidualData,
)
from .regression.regression_chart import (
    RegressionChart,
    RegressionDistributionChartData,
)
from .regression.regression_chart_data import (
    RegressionPredictedActualChartData,
    RegressionResidualBucketChartData,
    RegressionResidualScatterChartData,
)
from radicalbit_platform_sdk.models import ModelType


# ruff's check regarding list comprehension is removed in favor of greater readability in multiclass methods
# ruff: noqa: PERF401
class RadicalbitChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data=RbitChartData) -> EChartsRawWidget:
        model_type = data.model.model_type()

        match model_type:
            case ModelType.BINARY:
                return self._binary_distribution_chart(data=data)
            case ModelType.MULTI_CLASS:
                return self._multiclass_distribution_chart(data=data)
            case ModelType.REGRESSION:
                return self._regression_distribution_chart(data=data)
            case _:
                return

    def _binary_distribution_chart(self, data=RbitChartData) -> EChartsRawWidget:
        title = data.model.target().name
        ref_class_metrics = [
            data.model_dump() for data in data.reference.data_quality().class_metrics
        ]

        if data.current:
            cur_class_metrics = [
                data.model_dump() for data in data.current.data_quality().class_metrics
            ]

            return BinaryChart().distribution_chart(
                data=BinaryDistributionChartData(
                    title=title,
                    reference_data=ref_class_metrics,
                    current_data=cur_class_metrics,
                )
            )

        return BinaryChart().distribution_chart(
            data=BinaryDistributionChartData(
                title=title,
                reference_data=ref_class_metrics,
            )
        )

    def _multiclass_distribution_chart(self, data=RbitChartData) -> EChartsRawWidget:
        title = data.model.target().name
        ref_class_metrics = [
            data.model_dump() for data in data.reference.data_quality().class_metrics
        ]

        if data.current:
            cur_class_metrics = [
                data.model_dump() for data in data.current.data_quality().class_metrics
            ]

            return MultiClassificationChart().distribution_chart(
                data=MultiClassificationDistributionChartData(
                    title=title,
                    reference_data=ref_class_metrics,
                    current_data=cur_class_metrics,
                )
            )

        return MultiClassificationChart().distribution_chart(
            data=MultiClassificationDistributionChartData(
                title=title,
                reference_data=ref_class_metrics,
            )
        )

    def _regression_distribution_chart(self, data=RbitChartData) -> EChartsRawWidget:
        title = data.model.target().name
        ref_target_metrics = data.reference.data_quality().target_metrics

        if data.current:
            curr_target_metrics = data.current.data_quality().target_metrics

            return RegressionChart().distribution_chart(
                data=RegressionDistributionChartData(
                    title=title,
                    bucket_data=curr_target_metrics.histogram.buckets,
                    reference_data=curr_target_metrics.histogram.reference_values,
                    current_data=curr_target_metrics.histogram.current_values,
                )
            )

        return RegressionChart().distribution_chart(
            data=RegressionDistributionChartData(
                title=title,
                bucket_data=ref_target_metrics.histogram.buckets,
                reference_data=ref_target_metrics.histogram.reference_values,
            )
        )

    def numerical_feature_chart(self, data=RbitChartData) -> List[EChartsRawWidget]:
        chart_list = []

        if data.current:
            chart_list = [
                Chart().numerical_bar_chart(
                    data=NumericalBarChartData(
                        title=f.feature_name,
                        bucket_data=[
                            format(value, '.3f') for value in f.histogram.buckets
                        ],
                        reference_data=f.histogram.reference_values,
                        current_data=f.histogram.current_values,
                    )
                )
                for f in data.current.data_quality().feature_metrics
                if f.type == 'numerical'
            ]
        else:
            chart_list = [
                Chart().numerical_bar_chart(
                    data=NumericalBarChartData(
                        title=f.feature_name,
                        bucket_data=f.histogram.buckets,
                        reference_data=f.histogram.reference_values,
                    )
                )
                for f in data.reference.data_quality().feature_metrics
                if f.type == 'numerical'
            ]

        return widgets.VBox(chart_list)

    def predicted_actual_chart(self, data=RbitChartResidualData) -> EChartsRawWidget:
        if data.current is not None:
            cur_model_quality = data.current.model_quality().global_metrics
            targets = cur_model_quality.residuals.targets
            predictions = [
                [targets[idx], p]
                for idx, p in enumerate(cur_model_quality.residuals.predictions)
            ]
            regression_line = cur_model_quality.residuals.regression_line

            return RegressionChart().predicted_actual_chart(
                data=RegressionPredictedActualChartData(
                    scatter_data=predictions,
                    coefficient=regression_line.coefficient,
                    intercept=regression_line.intercept,
                    color='#3695d9',
                )
            )

        if data.reference is not None:
            ref_model_quality = data.reference.model_quality()
            targets = ref_model_quality.residuals.targets
            predictions = [
                [targets[idx], p]
                for idx, p in enumerate(ref_model_quality.residuals.predictions)
            ]
            regression_line = ref_model_quality.residuals.regression_line

            return RegressionChart().predicted_actual_chart(
                data=RegressionPredictedActualChartData(
                    scatter_data=predictions,
                    coefficient=regression_line.coefficient,
                    intercept=regression_line.intercept,
                )
            )

        return None

    def residual_scatter_chart(self, data=RbitChartResidualData) -> EChartsRawWidget:
        if data.current is not None:
            cur_model_quality = data.current.model_quality().global_metrics
            standardized_residuals = cur_model_quality.residuals.standardized_residuals
            predictions = [
                [p, standardized_residuals[idx]]
                for idx, p in enumerate(cur_model_quality.residuals.predictions)
            ]

            return RegressionChart().residual_scatter_chart(
                data=RegressionResidualScatterChartData(
                    scatter_data=predictions, color='#3695d9'
                )
            )

        if data.reference is not None:
            ref_model_quality = data.reference.model_quality()
            standardized_residuals = ref_model_quality.residuals.standardized_residuals
            predictions = [
                [p, standardized_residuals[idx]]
                for idx, p in enumerate(ref_model_quality.residuals.predictions)
            ]

            return RegressionChart().residual_scatter_chart(
                data=RegressionResidualScatterChartData(scatter_data=predictions)
            )

        return None

    def residual_bucket_chart(self, data=RbitChartResidualData) -> EChartsRawWidget:
        if data.current is not None:
            cur_model_quality = data.current.model_quality().global_metrics
            histogram = cur_model_quality.residuals.histogram

            bucket_data=[format(value, '.3f') for value in histogram.buckets]
            histogram_data=[format(value, '.3f') for value in histogram.values]

            return RegressionChart().residual_bucket_chart(
                data=RegressionResidualBucketChartData(
                    bucket_data=bucket_data,
                    values=histogram_data,
                    color='#3695d9',
                )
            )

        if data.reference is not None:
            ref_model_quality = data.reference.model_quality()
            histogram = ref_model_quality.residuals.histogram

            return RegressionChart().residual_bucket_chart(
                data=RegressionResidualBucketChartData(
                    bucket_data=histogram.buckets,
                    values=histogram.values,
                )
            )

        return None

    def mse_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.mse

        current_mse = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_mse = [
            [c.timestamp, str(format(data.reference.model_quality().mse, '.3f') if data.reference.model_quality().mse is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Mean squared error',
                reference_data=ref_mse,
                current_data=current_mse,
            )
        )

    def rmse_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.rmse

        current_rmse = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_rmse = [
            [c.timestamp, str(format(data.reference.model_quality().rmse, '.3f') if data.reference.model_quality().rmse is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Root mean squared error',
                reference_data=ref_rmse,
                current_data=current_rmse,
            )
        )

    def mae_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.mae

        current_mae = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_mae = [
            [c.timestamp, str(format(data.reference.model_quality().mae, '.3f') if data.reference.model_quality().mae is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Mean absolute error',
                reference_data=ref_mae,
                current_data=current_mae,
            )
        )

    def mape_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.mape

        current_mape = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_mape = [
            [c.timestamp, str(format(data.reference.model_quality().mape, '.3f') if data.reference.model_quality().mape is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Mean absolute percentage error',
                reference_data=ref_mape,
                current_data=current_mape,
            )
        )

    def r2_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.r2

        current_r2 = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_r2 = [
            [c.timestamp, str(format(data.reference.model_quality().r2, '.3f') if data.reference.model_quality().r2 is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='R-squared', reference_data=ref_r2, current_data=current_r2
            )
        )

    def adj_r2_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.adj_r2

        current_adj_r2 = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_adj_r2 = [
            [c.timestamp, str(format(data.reference.model_quality().adj_r2, '.3f') if data.reference.model_quality().adj_r2 is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Adjusted R-squared',
                reference_data=ref_adj_r2,
                current_data=current_adj_r2,
            )
        )

    def variance_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.variance

        current_variance = [[c.timestamp, str(format(c.value,'.3f') if c.value is not None else 0)] for c in current_model_quality]
        ref_variance = [
            [c.timestamp, str(format(data.reference.model_quality().variance, '.3f') if data.reference.model_quality().variance is not None else 0)]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Variance',
                reference_data=ref_variance,
                current_data=current_variance,
            )
        )

    def accuracy_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.accuracy

        current_accuracy = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_accuracy = [
            [c.timestamp, str(format(data.reference.model_quality().accuracy, '.3f'))]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Accuracy',
                reference_data=ref_accuracy,
                current_data=current_accuracy,
            )
        )

    def precision_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.precision

        current_precision = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_precision = [
            [c.timestamp, str(format(data.reference.model_quality().precision, '.3f'))]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Precision',
                reference_data=ref_precision,
                current_data=current_precision,
            )
        )

    def recall_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.recall

        current_recall = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_recall = [
            [c.timestamp, str(format(data.reference.model_quality().recall, '.3f'))]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Recall', reference_data=ref_recall, current_data=current_recall
            )
        )

    def f1_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.f1

        current_f1 = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_f1 = [
            [c.timestamp, str(format(data.reference.model_quality().f1, '.3f'))]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='F1', reference_data=ref_f1, current_data=current_f1
            )
        )

    def true_positive_rate_linear_chart(
        self, data=RbitChartLinearData
    ) -> EChartsRawWidget:
        current_model_quality = (
            data.current.model_quality().grouped_metrics.true_positive_rate
        )

        current_true_positive_rate = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_true_positive_rate = [
            [
                c.timestamp,
                str(format(data.reference.model_quality().true_positive_rate, '.3f')),
            ]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='True positive rate',
                reference_data=ref_true_positive_rate,
                current_data=current_true_positive_rate,
            )
        )

    def false_positive_rate_linear_chart(
        self, data=RbitChartLinearData
    ) -> EChartsRawWidget:
        current_model_quality = (
            data.current.model_quality().grouped_metrics.false_positive_rate
        )

        current_false_positive_rate = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_false_positive_rate = [
            [
                c.timestamp,
                str(format(data.reference.model_quality().false_positive_rate, '.3f')),
            ]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='False positive rate',
                reference_data=ref_false_positive_rate,
                current_data=current_false_positive_rate,
            )
        )

    def log_loss_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().grouped_metrics.log_loss
        if current_model_quality is None:
            return None

        current_log_loss = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_log_loss = [
            [c.timestamp, str(format(data.reference.model_quality().log_loss, '.3f'))]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='Log loss',
                reference_data=ref_log_loss,
                current_data=current_log_loss,
            )
        )

    def auc_roc_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = (
            data.current.model_quality().grouped_metrics.area_under_roc
        )

        if current_model_quality is None:
            return None

        current_auc_roc = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_auc_roc = [
            [
                c.timestamp,
                str(format(data.reference.model_quality().area_under_roc, '.3f')),
            ]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='AUC-ROC',
                reference_data=ref_auc_roc,
                current_data=current_auc_roc,
            )
        )

    def pr_auc_linear_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = (
            data.current.model_quality().grouped_metrics.area_under_pr
        )

        if current_model_quality is None:
            return None

        current_pr_auc = [
            [c.timestamp, str(format(c.value, '.3f') if c.value is not None else 0)]
            for c in current_model_quality
        ]
        ref_pr_auc = [
            [
                c.timestamp,
                str(format(data.reference.model_quality().area_under_pr, '.3f')),
            ]
            for c in current_model_quality
        ]

        return Chart().linear_chart(
            data=LinearChartData(
                title='PR AUC', reference_data=ref_pr_auc, current_data=current_pr_auc
            )
        )

    def multiclass_recall_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().class_metrics
        reference_model_quality = data.reference.model_quality().class_metrics

        current_data = [
            {
                'name': d.class_name,
                'values': [
                    [
                        k.timestamp,
                        str(format(k.value, '.3f') if k.value is not None else 0),
                    ]
                    for k in d.grouped_metrics.recall
                ],
            }
            for d in current_model_quality
        ]

        reference_data = []
        for d in current_model_quality:
            values = []
            for k in d.grouped_metrics.recall:
                for h in reference_model_quality:
                    if h.class_name is d.class_name:
                        values.append(
                            [k.timestamp, str(format(h.metrics.recall, '.3f'))]
                        )
            element = {'name': d.class_name, 'values': values}
            reference_data.append(element)

        return MultiClassificationChart().linear_chart(
            data=MultiClassificationLinearChartData(
                title='Recall', reference_data=reference_data, current_data=current_data
            )
        )

    def multiclass_f1_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().class_metrics
        reference_model_quality = data.reference.model_quality().class_metrics

        current_data = [
            {
                'name': d.class_name,
                'values': [
                    [
                        k.timestamp,
                        str(format(k.value, '.3f') if k.value is not None else 0),
                    ]
                    for k in d.grouped_metrics.f_measure
                ],
            }
            for d in current_model_quality
        ]

        reference_data = []
        for d in current_model_quality:
            values = []
            for k in d.grouped_metrics.f_measure:
                for h in reference_model_quality:
                    if h.class_name is d.class_name:
                        values.append(
                            [k.timestamp, str(format(h.metrics.f_measure, '.3f'))]
                        )
            element = {'name': d.class_name, 'values': values}
            reference_data.append(element)

        return MultiClassificationChart().linear_chart(
            data=MultiClassificationLinearChartData(
                title='F1', reference_data=reference_data, current_data=current_data
            )
        )

    def multiclass_precision_chart(self, data=RbitChartLinearData) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().class_metrics
        reference_model_quality = data.reference.model_quality().class_metrics

        current_data = [
            {
                'name': d.class_name,
                'values': [
                    [
                        k.timestamp,
                        str(format(k.value, '.3f') if k.value is not None else 0),
                    ]
                    for k in d.grouped_metrics.precision
                ],
            }
            for d in current_model_quality
        ]

        reference_data = []
        for d in current_model_quality:
            values = []
            for k in d.grouped_metrics.precision:
                for h in reference_model_quality:
                    if h.class_name is d.class_name:
                        values.append(
                            [k.timestamp, str(format(h.metrics.precision, '.3f'))]
                        )
            element = {'name': d.class_name, 'values': values}
            reference_data.append(element)

        return MultiClassificationChart().linear_chart(
            data=MultiClassificationLinearChartData(
                title='Precision',
                reference_data=reference_data,
                current_data=current_data,
            )
        )

    def multiclass_false_positive_rate_chart(
        self, data=RbitChartLinearData
    ) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().class_metrics
        reference_model_quality = data.reference.model_quality().class_metrics

        current_data = [
            {
                'name': d.class_name,
                'values': [
                    [
                        k.timestamp,
                        str(format(k.value, '.3f') if k.value is not None else 0),
                    ]
                    for k in d.grouped_metrics.false_positive_rate
                ],
            }
            for d in current_model_quality
        ]

        reference_data = []
        for d in current_model_quality:
            values = []
            for k in d.grouped_metrics.false_positive_rate:
                for h in reference_model_quality:
                    if h.class_name is d.class_name:
                        values.append(
                            [
                                k.timestamp,
                                str(format(h.metrics.false_positive_rate, '.3f')),
                            ]
                        )
            element = {'name': d.class_name, 'values': values}
            reference_data.append(element)

        return MultiClassificationChart().linear_chart(
            data=MultiClassificationLinearChartData(
                title='False positive rate',
                reference_data=reference_data,
                current_data=current_data,
            )
        )

    def multiclass_true_positive_rate_chart(
        self, data=RbitChartLinearData
    ) -> EChartsRawWidget:
        current_model_quality = data.current.model_quality().class_metrics
        reference_model_quality = data.reference.model_quality().class_metrics

        current_data = [
            {
                'name': d.class_name,
                'values': [
                    [
                        k.timestamp,
                        str(format(k.value, '.3f') if k.value is not None else 0),
                    ]
                    for k in d.grouped_metrics.true_positive_rate
                ],
            }
            for d in current_model_quality
        ]

        reference_data = []
        for d in current_model_quality:
            values = []
            for k in d.grouped_metrics.true_positive_rate:
                for h in reference_model_quality:
                    if h.class_name is d.class_name:
                        values.append(
                            [
                                k.timestamp,
                                str(format(h.metrics.true_positive_rate, '.3f')),
                            ]
                        )
            element = {'name': d.class_name, 'values': values}
            reference_data.append(element)

        return MultiClassificationChart().linear_chart(
            data=MultiClassificationLinearChartData(
                title='False positive rate',
                reference_data=reference_data,
                current_data=current_data,
            )
        )

    def confusion_matrix(self, data=RbitChartResidualData) -> EChartsRawWidget:
        model_type = data.model.model_type()

        match model_type:
            case ModelType.BINARY:
                if data.current is None:
                    global_metrics = data.reference.model_quality()
                    return Chart().confusion_matrix_chart(
                        data=ConfusionMatrixChartData(
                            axis_label=['1', '0'],
                            matrix=[
                                [
                                    global_metrics.true_positive_count,
                                    global_metrics.false_negative_count,
                                ],
                                [
                                    global_metrics.false_positive_count,
                                    global_metrics.true_negative_count,
                                ],
                            ],
                        )
                    )

                global_metrics = data.current.model_quality().global_metrics
                return Chart().confusion_matrix_chart(
                    data=ConfusionMatrixChartData(
                        axis_label=['1', '0'],
                        matrix=[
                            [
                                global_metrics.true_positive_count,
                                global_metrics.false_negative_count,
                            ],
                            [
                                global_metrics.false_positive_count,
                                global_metrics.true_negative_count,
                            ],
                        ],
                        color=['#FFFFFF', '#3695d9'],
                    )
                )

            case ModelType.MULTI_CLASS:
                if data.current is None:
                    model_quality = data.reference.model_quality()
                    return Chart().confusion_matrix_chart(
                        data=ConfusionMatrixChartData(
                            axis_label=model_quality.classes,
                            matrix=model_quality.global_metrics.confusion_matrix,
                        )
                    )

                model_quality = data.current.model_quality()

                return Chart().confusion_matrix_chart(
                    data=ConfusionMatrixChartData(
                        axis_label=model_quality.classes,
                        matrix=model_quality.global_metrics.confusion_matrix,
                        color=['#FFFFFF', '#3695d9'],
                    )
                )

            case _:
                return    

    def data_quality(self, data=RbitChartData) -> List[EChartsRawWidget]:
        distribution_chart = self.distribution_chart(data=data)
        numerical_feature_chart = self.numerical_feature_chart(data=data)

        return widgets.VBox([distribution_chart, numerical_feature_chart])

    def model_quality(self, data=RbitChartData) -> List[EChartsRawWidget]:
        model_type = data.model.model_type()

        match model_type:
            case ModelType.BINARY:
                if data.current is None:
                    confusion_matrix = self.confusion_matrix(data=data)
                    return widgets.VBox([confusion_matrix])

                accuracy_linear_chart = self.accuracy_linear_chart(data=data)
                precision_linear_chart = self.precision_linear_chart(data=data)
                recall_linear_chart = self.recall_linear_chart(data=data)
                f1_linear_chart = self.f1_linear_chart(data=data)
                true_positive_rate_linear_chart = self.true_positive_rate_linear_chart(
                    data=data
                )
                false_positive_rate_linear_chart = (
                    self.false_positive_rate_linear_chart(data=data)
                )
                log_loss_linear_chart = self.log_loss_linear_chart(data=data)
                confusion_matrix = self.confusion_matrix(data=data)
                auc_roc_linear_chart = self.auc_roc_linear_chart(data=data)
                pr_auc_linear_chart = self.pr_auc_linear_chart(data=data)

                return widgets.VBox(
                    [
                        accuracy_linear_chart,
                        precision_linear_chart,
                        recall_linear_chart,
                        f1_linear_chart,
                        true_positive_rate_linear_chart,
                        false_positive_rate_linear_chart,
                        log_loss_linear_chart,
                        confusion_matrix,
                        auc_roc_linear_chart,
                        pr_auc_linear_chart,
                    ]
                )

            case ModelType.MULTI_CLASS:
                if data.current is None:
                    confusion_matrix = self.confusion_matrix(data=data)
                    return widgets.VBox([confusion_matrix])

                confusion_matrix = self.confusion_matrix(data=data)
                multiclass_recall_chart = self.multiclass_recall_chart(data=data)
                multiclass_f1_chart = self.multiclass_f1_chart(data=data)
                multiclass_precision_chart = self.multiclass_precision_chart(data=data)
                multiclass_false_positive_rate_chart = (
                    self.multiclass_false_positive_rate_chart(data=data)
                )
                multiclass_true_positive_rate_chart = (
                    self.multiclass_true_positive_rate_chart(data=data)
                )

                return widgets.VBox(
                    [
                        confusion_matrix,
                        multiclass_recall_chart,
                        multiclass_f1_chart,
                        multiclass_precision_chart,
                        multiclass_false_positive_rate_chart,
                        multiclass_true_positive_rate_chart,
                    ]
                )

            case ModelType.REGRESSION:
                if data.current is None:
                    predicted_actual_chart = self.predicted_actual_chart(data=data)
                    residual_scatter_chart = self.residual_scatter_chart(data=data)
                    residual_bucket_chart = self.residual_bucket_chart(data=data)
                    return widgets.VBox(
                        [
                            predicted_actual_chart,
                            residual_scatter_chart,
                            residual_bucket_chart,
                        ]
                    )

                predicted_actual_chart = self.predicted_actual_chart(data=data)
                residual_scatter_chart = self.residual_scatter_chart(data=data)
                residual_bucket_chart = self.residual_bucket_chart(data=data)
                mse_linear_chart = self.mse_linear_chart(data=data)
                rmse_linear_chart = self.rmse_linear_chart(data=data)
                mae_linear_chart = self.mae_linear_chart(data=data)
                mape_linear_chart = self.mape_linear_chart(data=data)
                r2_linear_chart = self.r2_linear_chart(data=data)
                adj_r2_linear_chart = self.adj_r2_linear_chart(data=data)
                variance_linear_chart = self.variance_linear_chart(data=data)

                return widgets.VBox(
                    [
                        predicted_actual_chart,
                        residual_scatter_chart,
                        residual_bucket_chart,
                        mse_linear_chart,
                        rmse_linear_chart,
                        mae_linear_chart,
                        mape_linear_chart,
                        r2_linear_chart,
                        adj_r2_linear_chart,
                        variance_linear_chart,
                    ]
                )

            case _:
                return
