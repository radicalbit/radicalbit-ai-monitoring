from ipecharts import EChartsRawWidget

from ..utils import get_chart_header
from .binary_chart_data import BinaryDistributionChartData, BinaryLinearChartData


class BinaryChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data: BinaryDistributionChartData) -> EChartsRawWidget:
        assert len(data.reference_data) <= 2
        assert len(data.y_axis_label) <= 2

        if data.current_data:
            assert len(data.current_data) <= 2

        reference_json_data = [binary_data.model_dump() for binary_data in data.reference_data]
        current_data_json = [binary_data.model_dump() for binary_data in data.current_data] if data.current_data else []

        reference_series_data = {
            'title': data.title,
            'type': 'bar',
            'itemStyle': {'color': '#9B99A1'},
            'data': reference_json_data,
            'color': '#9B99A1',
            'name': 'Reference',
            'label': {
                'show': True,
                'position': 'insideRight',
                'fontWeight': 'bold',
                'color': '#FFFFFF',
            },
        }

        current_series_data = {
            'title': data.title + '_current',
            'type': 'bar',
            'itemStyle': {},
            'data': current_data_json,
            'color': '#3695d9',
            'name': 'Current',
            'label': {
                'show': True,
                'position': 'insideRight',
                'fontWeight': 'bold',
                'color': '#FFFFFF',
            },
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
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
            },
            'yAxis': {
                'type': 'category',
                'axisTick': {'show': False},
                'axisLine': {'show': False},
                'splitLine': {'show': False},
                'axisLabel': {'fontSize': 12, 'color': '#9B99A1'},
                'data': data.y_axis_label,
            },
            'emphasis': {'disabled': True},
            'barCategoryGap': '21%',
            'barGap': '0',
            'itemStyle': {'borderWidth': 1, 'borderColor': 'rgba(201, 25, 25, 1)'},
            'series': series,
        }

        option.update(get_chart_header(title=data.title))

        return EChartsRawWidget(option=option)

    def linear_chart(self, data: BinaryLinearChartData) -> EChartsRawWidget:

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
