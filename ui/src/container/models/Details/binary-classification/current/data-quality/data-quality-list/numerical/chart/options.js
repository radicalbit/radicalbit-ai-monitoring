import { numberFormatter } from '@Src/constants';

export default function chartOptions(dataset, referenceColor, currentColor) {
  const dataFormatted = dataset.buckets.map((value) => numberFormatter().format(value));
  const lastElementData = dataFormatted.pop();
  const xAxisData = dataFormatted.map((el, idx) => `[${dataFormatted[idx]}${(idx < dataFormatted.length - 1) ? `-${dataFormatted[idx + 1]})` : (idx === dataFormatted.length - 1) ? `-${lastElementData}]` : ''} `);

  return {
    grid: {
      top: 10,
      bottom: 0,
      left: 25,
      right: 5,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: { show: false },
      axisLabel: {
        fontSize: 12,
        interval: 0,
        rotate: 20,
        color: '#9b99a1',
      },
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
    },
    series: [
      {
        data: dataset.referenceValues,
        type: 'bar',
        itemStyle: { color: referenceColor },
      },
      {
        data: dataset.currentValues,
        type: 'bar',
        itemStyle: { color: currentColor },
      },
    ],
  };
}
