from ipecharts import EChartsRawWidget
from radicalbit_platform_chart_sdk.charts import ChartData, NumericalBarChartData


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

    def numerical_bar_chart(self, data: NumericalBarChartData) -> EChartsRawWidget:
        reference_data_json = {
                    "title": "reference",
                    "type": "bar",
                    "itemStyle": {
                        "color": "#9B99A1"
                    },
                    "data": data.reference_data
                }
        
        current_data_json = {
                    "title": "current",
                    "type": "bar",
                    "itemStyle": {
                        "color": "#3695D9"
                    },
                    "data": data.current_data
                }
        
        series = [reference_data_json] if not data.current_data else [reference_data_json, current_data_json]
        
        option = {
            "grid": {
                "left": 0,
                "right": 20,
                "bottom": 0,
                "top": 10,
                "containLabel": true
            },
            "xAxis": {
                "type": "category",
                "axisTick": {
                    "show": false
                },
                "axisLine": {
                    "show": false
                },
                "splitLine": {
                    "show": false
                },
                "axisLabel": {
                    "fontSize": 12,
                    "interval": 0,
                    "color": "#9B99A1",
                    "rotate": 20
                },
                "data": [
                    "[19,700-99,400) ",
                    "[99,400-179,000) ",
                    "[179,000-259,000) ",
                    "[259,000-339,000) ",
                    "[339,000-418,000) ",
                    "[418,000-498,000) ",
                    "[498,000-578,000) ",
                    "[578,000-657,000) ",
                    "[657,000-737,000) ",
                    "[737,000-817,000] "
                ]
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {
                    "fontSize": 9,
                    "color": "#9B99A1"
                },
                "splitLine": {
                    "lineStyle": {
                        "color": "#9f9f9f54"
                    }
                }
            },
            "emphasis": {
                "disabled": true
            },
            "barCategoryGap": "0",
            "barGap": "0",
            "itemStyle": {
                "borderWidth": 1,
                "borderColor": "rgba(201, 25, 25, 1)"
            },
            "series": [
                {
                    "title": "reference",
                    "type": "bar",
                    "itemStyle": {
                        "color": "#9B99A1"
                    },
                    "data": [
                        502,
                        982,
                        896,
                        356,
                        181,
                        44,
                        24,
                        10,
                        3,
                        2
                    ]
                }
            ]
        }

        return EChartsRawWidget(option=option)
