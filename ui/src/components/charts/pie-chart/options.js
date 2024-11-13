import { CHART_COLOR } from '@Helpers/common-chart-options';

export default function pieChartOptions({ currentData, referenceData }) {
  const options = {
    series: [
      {
        percentPrecision: 2,
        type: 'pie',
        radius: ['50%', '80%'],
        labelLine: {
          show: false,
        },
        emphasis: { disabled: true },
        data: [
          {
            value: currentData,
            name: 'Current',
            itemStyle: { color: CHART_COLOR.CURRENT },
            selected: true,
            label: { show: false },
          },
          {
            value: referenceData,
            name: 'Reference',
            itemStyle: { color: referenceData === 100 ? '#9b99a1' : '#f60000' },
            label: { show: false },
          },
        ],
      },

    ],
  };
  return options;
}
