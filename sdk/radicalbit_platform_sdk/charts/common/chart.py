from ipecharts import EChartsRawWidget
import numpy as np

from .chart_data import ConfusionMatrixChartData, LinearChartData, NumericalBarChartData
from .utils import get_chart_header, get_formatted_bucket_data


class Chart:
    def __init__(self) -> None:
        pass

    def numerical_bar_chart(self, data: NumericalBarChartData) -> EChartsRawWidget:
        
        
        bucket_data_formatted = get_formatted_bucket_data(bucket_data=data.bucket_data)

        reference_data_json = {
            'title': 'reference',
            'type': 'bar',
            'name': 'Reference',
            'itemStyle': {'color': '#9B99A1'},
            'data': data.reference_data,
        }

        current_data_json = {
            'title': 'current',
            'type': 'bar',
            'name': 'Current',
            'itemStyle': {'color': '#3695D9'},
            'data': data.current_data,
        }

        series = (
            [reference_data_json]
            if not data.current_data
            else [reference_data_json, current_data_json]
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
                    'color': '#9B99A1',
                    'rotate': 20,
                },
                'data': bucket_data_formatted,
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9B99A1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
            },
            'emphasis': {'disabled': True},
            'barCategoryGap': '0',
            'barGap': '0',
            'itemStyle': {'borderWidth': 1, 'borderColor': 'rgba(201, 25, 25, 1)'},
            'series': series,
        }

        option.update(get_chart_header(title=data.title)) 

        return EChartsRawWidget(option=option)

    def confusion_matrix_chart(
        self, data: ConfusionMatrixChartData
    ) -> EChartsRawWidget:
        
        assert len(data.matrix) == len(data.axis_label) * len(
            data.axis_label
        ), 'axis_label count and matrix item count are not compatibile'

        np_matrix = np.matrix(data.matrix)

        options = {
            'yAxis': {
                'type': 'category',
                'axisTick': {'show': False},
                'axisLine': {'show': False},
                'splitLine': {'show': False},
                'axisLabel': {'fontSize': 12, 'color': '#9B99A1'},
                'data': data.axis_label,
                'name': 'Actual',
                'nameGap': 25,
                'nameLocation': 'middle',
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
                    'rotate': 45,
                },
                'data': data.axis_label.reverse(),
                'name': 'Predicted',
                'nameGap': 25,
                'nameLocation': 'middle',
            },
            'grid': {'bottom': 60, 'top': 0, 'left': 44, 'right': 80},
            'emphasis': {'disabled': True},
            'axis': {'axisLabel': {'fontSize': 9, 'color': '#9b99a1'}},
            'visualMap': {
                'calculable': True,
                'orient': 'vertical',
                'right': 'right',
                'top': 'center',
                'itemHeight': '250rem',
                'max': np_matrix.max(),
                'inRange': {'color': data.color},
            },
            'series': {
                'name': '',
                'type': 'heatmap',
                'label': {'show': True},
                'data': data.matrix,
            },
        }

        return EChartsRawWidget(option=options)

    def linear_chart(self, data: LinearChartData) -> EChartsRawWidget:

        reference_series_data = {
            'name': 'Reference',
            'type': 'line',
            'lineStyle': {'width': 2.2, 'color': '#9B99A1', 'type': 'dotted'},
            'symbol': 'none',
            'data': data.reference_data,
            'itemStyle': {'color': '#9B99A1'},
            'endLabel': {'show': True, 'color': '#9B99A1'},
            'color': '#9B99A1',
        }

        current_series_data = {
            'name': data.title,
            'type': 'line',
            'lineStyle': {'width': 2.2, 'color': '#73B2E0'},
            'symbol': 'none',
            'data': data.current_data,
            'itemStyle': {'color': '#73B2E0'},
        }

        series = [reference_series_data, current_series_data]

        options = {
            'tooltip': {
                'trigger': 'axis',
                'crosshairs': True,
                'axisPointer': {'type': 'cross', 'label': {'show': True}},
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
                'scale': True,
            },
            'xAxis': {
                'type': 'time',
                'axisTick': {'show': False},
                'axisLine': {'show': False},
                'splitLine': {'show': False},
                'axisLabel': {'fontSize': 12, 'color': '#9b99a1'},
                'scale': True,
            },
            'grid': {
                'bottom': 0,
                'top': 32,
                'left': 0,
                'right': 64,
                'containLabel': True,
            },
            'series': series,
            'legend': {
                'show': True,
                'textStyle': {'color': '#9B99A1'},
            },
        }

        options.update(get_chart_header(title=data.title))

        return EChartsRawWidget(option=options)
