import { CHART_TYPE, gridOptions } from '@Helpers/common-chart-options';
import dayjs from 'dayjs';

export default function lineChartOptions(title, color, values) {
  const xAxisData = values.map(({ startDate }) => startDate);
  const seriesData = values.map(({ count }) => count);

  return {
    ...gridOptions(CHART_TYPE.LINE),
    tooltip: {
      trigger: 'axis',
      formatter: ([{ marker, name, value }]) => `
      <div>
        <div>${dayjs(name).format('YYYY-MM-DD HH:mm:ss')}</div>
        <div>
          <span>${marker}</span>
          <span>${value}</value>
        </div>
      </div>`,
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLabel: {
        formatter: (date) => dayjs(date).format('YYYY-MM-DD HH:mm:ss'),
      },
      scale: true,
    },
    yAxis: {
      type: 'value',
      scale: true,
    },
    series: [
      {
        data: seriesData,
        type: 'line',
        smooth: true,
      },
    ],
  };
}
