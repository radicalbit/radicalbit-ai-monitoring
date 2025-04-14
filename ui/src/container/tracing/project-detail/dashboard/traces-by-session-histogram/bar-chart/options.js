import { CHART_TYPE, gridOptions } from '@Helpers/common-chart-options';
// import dayjs from 'dayjs';

export default function lineChartOptions(title, color, values) {
  const sessionUuids = values.map(({ sessionUuid }) => sessionUuid);
  const counts = values.map(({ count }) => count);

  return {
    ...gridOptions(CHART_TYPE.BAR),

    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.01],
    },
    yAxis: {
      type: 'category',
      data: sessionUuids, // Replace with dynamic keys from your data
      axisLabel: { show: false },
    },
    series: [
      {
        type: 'bar',
        data: counts, // Replace with dynamic counts from your data
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}',
          color: '#000', // Black label color
          fontSize: 14, // Bigger font size
          fontWeight: 400, // Lighter font weight
        },
        itemStyle: {
          color: '#3695D9', // Blue bar color
          borderRadius: [0, 5, 5, 0], // Optional: Rounded corners for bars
        },
      },
    ],
  };
}
