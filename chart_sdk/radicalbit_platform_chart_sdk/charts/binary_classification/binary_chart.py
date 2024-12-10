from ipecharts import EChartsRawWidget

from .binary_chart_data import BinaryChartData


class BinaryChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data: BinaryChartData) -> EChartsRawWidget:
        reference_json_data = data.model_dump().get('reference_data')
        current_data_json =  data.model_dump().get('current_data')

        reference_series_data = {
            "title": data.title,
            "type": "bar",
            "itemStyle": {
                "color": "#9B99A1"
            },
            "data": reference_json_data,
            "color": "#9B99A1",
            "name": "Reference",
            "label": {
                "show": True,
                "position": "insideRight",
                "fontWeight": "bold",
                "color": "#FFFFFF"
            }
        }

        current_series_data = {
            "title": data.title,
            "type": "bar",
            "itemStyle": {},
            "data": current_data_json,
            "color": "#3695d9",
            "label": {
                "show": True,
                "position": "insideRight",
                "fontWeight": "bold",
                "color": "#FFFFFF"
            }
        }

        series = [reference_series_data] if not data.current_data else [reference_series_data, current_series_data]

        option = {
            "grid": {
                "left": 0,
                "right": 20,
                "bottom": 0,
                "top": 10,
                "containLabel": True
            },
            "xAxis": {
                "type": "value",
                "axisLabel": {
                    "fontSize": 9,
                    "color": "#9b99a1"
                },
                "splitLine": {
                    "lineStyle": {
                        "color": "#9f9f9f54"
                    }
                }
            },
            "yAxis": {
                "type": "category",
                "axisTick": {
                    "show": False
                },
                "axisLine": {
                    "show": False
                },
                "splitLine": {
                    "show": False
                },
                "axisLabel": {
                    "fontSize": 12,
                    "color": "#9B99A1"
                },
                "data": [
                    "0.0",
                    "1.0"
                ]
            },
            "emphasis": {
                "disabled": True
            },
            "barCategoryGap": "21%",
            "barGap": "0",
            "itemStyle": {
                "borderWidth": 1,
                "borderColor": "rgba(201, 25, 25, 1)"
            },
            "series": series
        }

        return EChartsRawWidget(option=option)

