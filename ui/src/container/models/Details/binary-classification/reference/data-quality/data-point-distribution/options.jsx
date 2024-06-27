import { CHART_COLOR } from '@Container/models/Details/constants';
import { numberFormatter } from '@Src/constants';

export default function chartOptions(title, dataset) {
  const yAxisLabel = dataset.map(({ name }) => name);

  return {
    grid: {
      left: 0,
      right: 20,
      bottom: 0,
      top: 0,
      containLabel: true,
    },
    xAxis: {
      type: 'value',
      boundaryGap: true,
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
    },
    yAxis: {
      type: 'category',
      data: yAxisLabel,
      boundaryGap: true,
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: { show: false },
      axisLabel: {
        fontSize: 10,
      },
    },
    emphasis: {
      disabled: true,
    },
    barCategoryGap: '21%',
    overflow: 'truncate',
    lineOverflow: 'truncate',
    series: [
      {
        name: title,
        type: 'bar',
        color: CHART_COLOR.REFERENCE_LIGHT,
        emphasis: {
          focus: 'series',
        },
        label: {
          show: true,
          position: 'insideRight',
          fontWeight: 'bold',
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
        data: dataset.map(({ count, percentage }) => ({ percentage, count, value: count })),
      },
    ],
  };
}
