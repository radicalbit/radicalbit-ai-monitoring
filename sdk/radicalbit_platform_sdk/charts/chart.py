from ipecharts import EChartsRawWidget


class Chart:
    def __init__(self) -> None:
        pass
    def placeholder_chart(self) -> EChartsRawWidget:
        option = {
            'xAxis': {
                'type': 'category',
                'boundaryGap': False,
                'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            'yAxis': {
                'type': 'value'
            },
            'series': [
                {
                    'data': [820, 932, 901, 934, 1290, 1330, 1320],
                    'type': 'line',
                    'areaStyle': {}
                }
            ]
        }

        return EChartsRawWidget(option=option)

""" refernceData = api.getRefence
currentData = api.getRefence

linearChart = Chart.LinearCHart(reference,current)

linearChart.plot() """