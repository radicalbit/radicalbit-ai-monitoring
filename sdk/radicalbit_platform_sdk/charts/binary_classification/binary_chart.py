from ipecharts import EChartsRawWidget

from ..common.utils import get_chart_header
from .binary_chart_data import BinaryDistributionChartData


class BinaryChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data: BinaryDistributionChartData) -> EChartsRawWidget:
        assert len(data.reference_data) <= 2

        if data.current_data:
            assert len(data.current_data) <= 2

        y_axis_label = [
            metric['name']
            for metric in [
                binary_data.model_dump() for binary_data in data.reference_data
            ]
        ]

        reference_data = [
            {
                'percentage': metric.percentage,
                'value': metric.count,
                'count': metric.count,
            }
            for metric in data.reference_data
        ]

        current_data = (
            [
                {
                    'percentage': metric.percentage,
                    'value': metric.count,
                    'count': metric.count,
                }
                for metric in data.current_data
            ]
            if data.current_data
            else []
        )

        reference_series_data = {
            'title': data.title,
            'type': 'bar',
            'itemStyle': {'color': '#9B99A1'},
            'data': reference_data,
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
            'data': current_data,
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
                'data': y_axis_label,
            },
            'emphasis': {'disabled': True},
            'barCategoryGap': '21%',
            'barGap': '0',
            'itemStyle': {'borderWidth': 1, 'borderColor': 'rgba(201, 25, 25, 1)'},
            'series': series,
        }

        option.update(get_chart_header(title=data.title))

        return EChartsRawWidget(option=option)
