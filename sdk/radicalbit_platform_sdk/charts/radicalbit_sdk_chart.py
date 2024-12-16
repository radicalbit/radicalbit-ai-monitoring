from typing import List
from ipecharts import EChartsRawWidget

from radicalbit_platform_sdk.charts.binary_classification import BinaryChart, BinaryDistributionChartData
from radicalbit_platform_sdk.charts.common.chart import Chart
from radicalbit_platform_sdk.charts.common.chart_data import NumericalBarChartData
from radicalbit_platform_sdk.charts.radicalbit_sdk_chart_data import RbitChartData
from radicalbit_platform_sdk.models import ModelType
import ipywidgets as widgets


class RadicalbitChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data=RbitChartData) -> EChartsRawWidget:
        model_type = data.model.model_type()

        match model_type:
            case ModelType.BINARY:
                return self._binary_distribution_chart(data=data)
            case ModelType.MULTI_CLASS:
                return self._binary_distribution_chart(data=data)
            case ModelType.REGRESSION:
                return self._binary_distribution_chart(data=data)

    def _binary_distribution_chart(self, data=RbitChartData) -> EChartsRawWidget:
        title = data.model.target().name
        ref_class_metrics = [data.model_dump() for data in data.reference.data_quality().class_metrics]

        if data.current:
            cur_class_metrics = [
                data.model_dump() for data in data.current.data_quality().class_metrics]

            return BinaryChart().distribution_chart(data=BinaryDistributionChartData(
                title=title,
                reference_data=ref_class_metrics,
                current_data=cur_class_metrics
            ))
        else:
            return BinaryChart().distribution_chart(data=BinaryDistributionChartData(
                title=title,
                reference_data=ref_class_metrics,
            ))

    def numerical_feature_chart(self, data=RbitChartData) -> List[EChartsRawWidget]:
        chart_list = []
 
        if data.current:
            chart_list = [
                Chart().numerical_bar_chart(data=
                    NumericalBarChartData(
                        title=f.feature_name,
                        bucket_data=f.histogram.buckets,
                        reference_data=f.histogram.reference_values,
                        current_data=f.histogram.current_values
                    )
                ) for f in data.current.data_quality().feature_metrics if f.type == 'numerical'
            ]
        else:
            chart_list = [
                Chart().numerical_bar_chart(data=
                    NumericalBarChartData(
                        title=f.feature_name,
                        bucket_data=f.histogram.buckets,
                        reference_data=f.histogram.reference_values,
                    )
                ) for f in data.reference.data_quality().feature_metrics if f.type == 'numerical'
            ]
            
        return widgets.VBox(chart_list)
    

    
