from ipecharts import EChartsRawWidget

from radicalbit_platform_sdk.charts.binary_classification import BinaryChart, BinaryDistributionChartData
from .radicalbit_sdk_chart_data import RbitDistributionData
from radicalbit_platform_sdk.models import ModelType

class RadicalbitChart:
    def __init__(self) -> None:
        pass

    def DistributionChart(self,data=RbitDistributionData) -> EChartsRawWidget:

        print(data.model)

        match data.model_type:
            case ModelType.BINARY:
                return self.BinaryDistributionChart(data=data)
            case ModelType.MULTI_CLASS:
                return self.BinaryDistributionChart(data=data)
            case ModelType.REGRESSION:
                return self.BinaryDistributionChart(data=data)

    def BinaryDistributionChart(self,data=RbitDistributionData ) -> EChartsRawWidget:

        ref_class_metrics = [data.model_dump() for data in data.reference_data.class_metrics]

        if data.current_data:
            cur_class_metrics = [data.model_dump() for data in data.current_data.class_metrics]

            return BinaryChart().distribution_chart(data=
                BinaryDistributionChartData(
                    title=data.title,
                    reference_data=ref_class_metrics,
                    current_data=cur_class_metrics
                )
            )
        else:
            return BinaryChart().distribution_chart(data=
                BinaryDistributionChartData(
                    title=data.title,
                    reference_data=ref_class_metrics,
                )
            )
        
