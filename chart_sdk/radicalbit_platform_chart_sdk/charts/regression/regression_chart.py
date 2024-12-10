from ipecharts import EChartsRawWidget

from ..utils import get_formatted_bucket_data,get_chart_header
from .regression_chart_data import RegressionChartData


class RegressionChart:
    def __init__(self) -> None:
        pass

    def distribution_chart(self, data: RegressionChartData) -> EChartsRawWidget:
        bucket_data_formatted = get_formatted_bucket_data(bucket_data=data.bucket_data)

        reference_json_data = data.model_dump().get('reference_data')
        current_data_json = data.model_dump().get('current_data')

        reference_series_data = {
            "title": "reference",
            "type": "bar",
            "name":"Reference",
            "itemStyle": {
                "color": "#9B99A1"
            },
            "data": reference_json_data
        }

        current_series_data = {
            "title": "current",
            "type": "bar",
            "name":"Current",
            "itemStyle": {
                "color": "#3695d9"
            },
            "data": current_data_json
        }

        series = [reference_series_data] if not data.current_data else [
            reference_series_data, current_series_data]

        option = {
            "grid": {
                "left": 0,
                "right": 20,
                "bottom": 0,
                "top": 40,
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
                    "rotate": 20
                },
                "data":bucket_data_formatted,
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
            "barCategoryGap": "0",
            "barGap": "0",
            "itemStyle": {
                "borderWidth": 1,
                "borderColor": "rgba(201, 25, 25, 1)"
            },
            "series": series
        }

        option.update(get_chart_header(title=data.title))

        return EChartsRawWidget(option=option)
