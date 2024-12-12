from ipecharts import EChartsRawWidget
from IPython.display import display

from ..utils import get_chart_header
from .multi_class_chart_data import (
    MultiClassificationDistributionChartData,
    MultiClassificationLinearChartData,
)


class MultiClassificationChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(
        self, data: MultiClassificationDistributionChartData
    ) -> EChartsRawWidget:

        reference_json_data = [multi_class_data.model_dump() for multi_class_data in data.reference_data]
        current_data_json = [multi_class_data.model_dump() for multi_class_data in data.current_data] if data.current_data else []

        reference_series_data = {
            'title': data.title,
            'type': 'bar',
            'name': 'Reference',
            'itemStyle': {'color': '#9B99A1'},
            'data': reference_json_data,
        }

        current_series_data = {
            'title': data.title + '_current',
            'type': 'bar',
            'name': 'Current',
            'itemStyle': {'color': '#3695d9'},
            'data': current_data_json,
        }

        series = (
            [reference_series_data]
            if not data.current_data
            else [reference_series_data, current_series_data]
        )

        option = {
            'grid': {
                'left': 0,
                'right': 20,
                'bottom': 0,
                'top': 40,
                'containLabel': True,
            },
            'xAxis': {
                'type': 'category',
                'axisTick': {'show': False},
                'axisLine': {'show': False},
                'splitLine': {'show': False},
                'axisLabel': {
                    'fontSize': 12,
                    'interval': 0,
                    'color': '#9b99a1',
                    'rotate': 35,
                },
                'data': data.x_axis_label,
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
            },
            'emphasis': {'disabled': True},
            'barCategoryGap': '21%',
            'barGap': '0',
            'itemStyle': {'borderWidth': 1, 'borderColor': 'rgba(201, 25, 25, 1)'},
            'tooltip': {
                'trigger': 'axis',
                'crosshairs': True,
                'axisPointer': {'type': 'cross', 'label': {'show': True}},
            },
            'series': series,
        }

        option.update(get_chart_header(title=data.title))

        return EChartsRawWidget(option=option)

    def linear_chart(
        self, data: MultiClassificationLinearChartData
    ) -> EChartsRawWidget:

        series_current_data = [{
                    'name': element.name,
                    'type': 'line',
                    'lineStyle': {'width': 2.2},
                    'symbol': 'none',
                    'data': element.values,
                } for element in data.current_data ]

        series_reference_data = [ {
                    'name': element.name,
                    'type': 'line',
                    'lineStyle': {'width': 2, 'type': 'dotted'},
                    'symbol': 'none',
                    'data': element.values,
                    'endLabel': {
                        'show': True,
                        'color': '#9B99A1',
                    },
                } for element in data.reference_data]


        series = series_current_data + series_reference_data

        options = {
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
            },
            'xAxis': {
                'type': 'time',
                'axisTick': {'show': False},
                'axisLine': {'show': False},
                'splitLine': {'show': False},
                'axisLabel': {'fontSize': 12, 'color': '#9b99a1'},
            },
            'grid': {
                'bottom': 0,
                'top': 32,
                'left': 0,
                'right': 140,
                'containLabel': True,
            },
            'color': [
                '#00BFFF',
                '#1E90FF',
                '#00CED1',
                '#20B2AA',
                '#4169E1',
                '#6A5ACD',
                '#8A2BE2',
                '#9400D3',
                '#BA55D3',
            ],
            'legend': {
                'right': 0,
                'top': 16,
                'bottom': 0,
                'orient': 'vertical',
                'type': 'scroll',
                'scrollDataIndex': 'scroll',
                'pageIconSize': 8,
                'pageTextStyle': {'fontSize': 9, 'color': '#9b99a1'},
                'textStyle': {'fontSize': 9, 'color': '#9B99A1', 'fontWeight': '300'},
            },
            'tooltip': {'trigger': 'axis'},
            'emphasis': {'focus': 'series'},
            'title': {
                'text': '••• Reference',
                'textStyle': {'fontSize': 10, 'fontWeight': '300', 'color': '#9B99A1'},
                'right': 0,
            },
            'series': series,
        }

        display(data.title)

        return EChartsRawWidget(option=options)
