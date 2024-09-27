import { CHART_COLOR } from '@Helpers/common-chart-options';

export default function pieChartOptions({ currentData, referenceData }) {
  const options = {

    series: [
      {
        percentPrecision: 2,
        type: 'pie',
        radius: ['65%', '95%'],
        label: {
          show: true,
          fontSize: '20',
          fontWeight: 'bold',
          color: CHART_COLOR.WHITE,
          position: 'center',
          formatter: ({ data: { value } }) => `${value}%`,
        },
        labelLine: {
          show: false,
        },
        emphasis: { disabled: true },
        data: [
          { value: currentData, name: 'Current', itemStyle: { color: CHART_COLOR.CURRENT } },
          { value: referenceData, name: 'Reference', itemStyle: { color: '#f60000' } },
        ],
      },

    ],
  };
  return options;
}
