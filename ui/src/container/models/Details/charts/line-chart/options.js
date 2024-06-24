import { numberFormatter } from '@Src/constants';
import moment from 'moment';
import { CHART_COLOR } from '@Container/models/Details/constants';

export default function lineChartOptions(title, color, currentDataset, referenceDataset) {
  const series = [
    {
      name: title,
      type: 'line',
      lineStyle: {
        width: 2,
        color: '#73B2E0',
      },
      data: currentDataset.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]),
      symbol: 'none',
    },
  ];
  if (referenceDataset) {
    series.push({
      name: 'Reference',
      type: 'line',
      endLabel: {
        show: true,
        color: CHART_COLOR.REFERENCE,
        formatter: ({ value }) => `Reference\n${value[1]}`,
      },
      color: CHART_COLOR.REFERENCE,
      lineStyle: {
        width: 2,
        type: 'dotted',
        color: CHART_COLOR.REFERENCE,
      },
      data: referenceDataset.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]),
      symbol: 'none',
    });
  }

  return {
    color: [color],
    tooltip: {
      trigger: 'axis',
    },
    yAxis: [{
      type: 'value',
      boundaryGap: true,
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
    }],
    xAxis: [
      {
        type: 'time',
        axisLabel: {
          formatter: (value) => moment(+value).format('DD MMM HH.mm'),
          fontSize: 10,
          color: '#9b99a1',
        },
        axisTick: { show: false },
        axisLine: { show: false },
        splitLine: { show: false },

      },
    ],
    grid: {
      bottom: 0,
      top: 16,
      left: 0,
      right: 64,
      containLabel: true,
    },

    series,
  };
}
