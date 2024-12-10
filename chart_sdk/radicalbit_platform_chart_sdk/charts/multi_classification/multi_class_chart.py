from ipecharts import EChartsRawWidget
from .multi_class_chart_data import MultiClasssificationChartData


class MultiClassificationChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data: MultiClasssificationChartData) -> EChartsRawWidget:
        reference_json_data = data.model_dump().get('reference_data')
        current_data_json = data.model_dump().get('current_data')

        reference_series_data = {
            "title": data.title,
            "type": "bar",
            "itemStyle": {
                "color": "#9B99A1"
            },
            "data": reference_json_data
        }
        
        current_series_data = {
            "title": data.title + "_current",
            "type": "bar",
            "itemStyle": {
                "color": "#3695d9"
            },
            "data": current_data_json
        }
        
        series = [reference_series_data] if not data.current_data else [reference_series_data, current_series_data]

        option = {
            "grid": {
                "left": 0,
                "right": 20,
                "bottom": 0,
                "top": 25,
                "containLabel": True
            },
            "xAxis": {
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
                    "interval": 0,
                    "color": "#9b99a1",
                    "rotate": 35
                },
                "data": [
                    "0",
                    "1",
                    "2"
                ]
            },
            "yAxis": {
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
            "emphasis": {
                "disabled": True
            },
            "barCategoryGap": "21%",
            "barGap": "0",
            "itemStyle": {
                "borderWidth": 1,
                "borderColor": "rgba(201, 25, 25, 1)"
            },
            "tooltip": {
                "trigger": "axis",
                "crosshairs": True,
                "axisPointer": {
                    "type": "cross",
                    "label": {
                        "show": True
                    }
                }
            },
            "series": series
        }

        return EChartsRawWidget(option=option)
