from ipecharts import EChartsRawWidget
import numpy as np

from ..utils import get_chart_header, get_formatted_bucket_data
from .regression_chart_data import (
    RegressionDistributionChartData,
    RegressionPredictedActualChartData,
    RegressionResidualBucketChartData,
    RegressionResidualScatterChartData,
)


class RegressionChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(
        self, data: RegressionDistributionChartData
    ) -> EChartsRawWidget:
        bucket_data_formatted = get_formatted_bucket_data(bucket_data=data.bucket_data)

        reference_json_data = data.model_dump().get('reference_data')
        current_data_json = data.model_dump().get('current_data')

        reference_series_data = {
            'title': 'reference',
            'type': 'bar',
            'name': 'Reference',
            'itemStyle': {'color': '#9B99A1'},
            'data': reference_json_data,
        }

        current_series_data = {
            'title': 'current',
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
                    'rotate': 20,
                },
                'data': bucket_data_formatted,
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
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

    def predicted_actual_chart(
        self, data: RegressionPredictedActualChartData
    ) -> EChartsRawWidget:
        np_array = np.array(data.scatter_data)
        x_max = np_array.max()
        x_min = np_array.min()

        regression_line_data = [
            [x_min, (data.coefficient * x_min) + data.intercept],
            [x_max, (data.coefficient * x_max) + data.intercept],
        ]

        diagonal_line_data = [[x_min, x_min], [x_max, x_max]]

        options = {
            'grid': {
                'left': 20,
                'right': 0,
                'bottom': 50,
                'top': 24,
                'containLabel': True,
            },
            'xAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
                'name': 'ground_truth',
                'nameGap': 25,
                'nameLocation': 'middle',
                'scale': True,
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
                'name': 'prediction',
                'nameGap': 25,
                'nameLocation': 'middle',
                'scale': True,
            },
            'tooltip': {
                'axisPointer': {
                    'show': True,
                    'type': 'cross',
                    'lineStyle': {'type': 'dashed', 'width': 1},
                }
            },
            'series': [
                {
                    'name': '',
                    'type': 'scatter',
                    'emphasis': {'focus': 'series'},
                    'color': data.color,
                    'data': data.scatter_data,
                },
                {
                    'name': 'Diagonal line',
                    'type': 'line',
                    'lineStyle': {'width': 2.2, 'color': '#FFC000'},
                    'symbol': 'none',
                    'data': diagonal_line_data,
                    'itemStyle': {'color': '#FFC000'},
                },
                {
                    'name': 'Regression line',
                    'type': 'line',
                    'lineStyle': {'width': 2.2, 'color': '#8D6ECF'},
                    'symbol': 'none',
                    'data': regression_line_data,
                    'itemStyle': {'color': '#8D6ECF'},
                },
            ],
            'legend': {'show': True, 'textStyle': {'color': '#9B99A1'}, 'right': 0},
        }

        # TODO: the next print are required to show the title passed by params.
        # we disable the ruff check for this line, for now
        # Maybe exsist a better way to do this
        print('\033[1m' + 'prediction vs ground_truth') # noqa: T201

        return EChartsRawWidget(option=options)

    def residual_scatter_chart(
        self, data: RegressionResidualScatterChartData
    ) -> EChartsRawWidget:
        options = {
            'grid': {
                'left': 20,
                'right': 0,
                'bottom': 50,
                'top': 24,
                'containLabel': True,
            },
            'xAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
                'name': 'prediction',
                'nameGap': 25,
                'nameLocation': 'middle',
                'axisLine': {'lineStyle': {'width': 2, 'type': 'dashed'}},
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
                'name': 'standardized residuals',
                'nameGap': 25,
                'nameLocation': 'middle',
                'scale': False,
            },
            'tooltip': {
                'axisPointer': {
                    'show': True,
                    'type': 'cross',
                    'lineStyle': {'type': 'dashed', 'width': 1},
                }
            },
            'series': [
                {
                    'name': '',
                    'type': 'scatter',
                    'emphasis': {'focus': 'series'},
                    'color': data.color,
                    'data': data.scatter_data,
                }
            ],
        }

        return EChartsRawWidget(option=options)

    def residual_bucket_chart(
        self, data: RegressionResidualBucketChartData
    ) -> EChartsRawWidget:
        bucket_data_formatted = get_formatted_bucket_data(bucket_data=data.bucket_data)

        options = {
            'grid': {
                'left': 0,
                'right': 20,
                'bottom': 0,
                'top': 10,
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
                    'rotate': 20,
                },
                'data': bucket_data_formatted,
            },
            'yAxis': {
                'type': 'value',
                'axisLabel': {'fontSize': 9, 'color': '#9b99a1'},
                'splitLine': {'lineStyle': {'color': '#9f9f9f54'}},
            },
            'emphasis': {'disabled': True},
            'barCategoryGap': '0',
            'barGap': '0',
            'itemStyle': {'borderWidth': 1, 'borderColor': 'rgba(201, 25, 25, 1)'},
            'series': [
                {'type': 'bar', 'itemStyle': {'color': '#3695d9'}, 'data': data.values}
            ],
        }

        return EChartsRawWidget(option=options)