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
            label: {
              show: true,
              fontSize: '14',
              fontWeight: 'bold',
              color: CHART_COLOR.WHITE,
              position: 'center',
              formatter: ({ data: { value } }) => value === 0 ? '--' : `${value}%`,
            },
          },
          {
            value: referenceData,
            name: 'Reference',
            itemStyle: { color: referenceData === 100 ? '#1e2b43' : '#f60000' },
            label: { show: false },
          },
        ],
      },

    ],
  };
  return options;
}
