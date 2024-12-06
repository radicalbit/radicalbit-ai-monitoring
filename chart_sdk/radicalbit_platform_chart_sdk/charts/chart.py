from ipecharts import EChartsRawWidget
from radicalbit_platform_chart_sdk.charts import ChartData


class Chart:
    def __init__(self) -> None:
        pass

    def placeholder_chart(self, data: ChartData) -> EChartsRawWidget:
        option = {
            'xAxis': {
                'type': 'category',
                'boundaryGap': False,
                'data': data.x_axis_data,
            },
            'yAxis': {'type': 'value'},
            'series': [{'data': data.series_data, 'type': 'line', 'areaStyle': {}}],
        }

        return EChartsRawWidget(option=option)
