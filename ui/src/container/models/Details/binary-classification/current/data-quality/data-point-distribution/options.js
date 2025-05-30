import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';

export default function chartOptions(title, referenceDataset, currentDataset) {
  const yAxisLabel = currentDataset?.map(({ name }) => name);

  const referenceData = referenceDataset.map(({ count, percentage }) => ({ percentage, count, value: percentage }));
  const currentData = currentDataset.map(({ count, percentage }) => ({ percentage, count, value: percentage }));

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.PERCENTAGE),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.CATEGORY, yAxisLabel),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),
    tooltip: {
      ...commonChartOptions.tooltipOptions(CHART_TYPE.BAR),
      formatter: (params) => `
      ${params.marker} <strong>Class:</strong> ${params.name}
      <br/>
      <table style="margin-top:4px">
        <tr>
          <td style="padding-right:10px"><strong>Count</strong></td>
          <td style="text-align:right">${params.data.count}</td>
        </tr>
        <tr>
          <td style="padding-right:10px"><strong>Perc</strong></td>
          <td style="text-align:right">${(params.data.value * 100).toFixed(0)}%</td>
        </tr>
      </table>
    `,
    },
    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
        color: CHART_COLOR.REFERENCE_LIGHT,
        label: {
          show: true,
          position: 'insideRight',
          fontWeight: 'bold',
          color: CHART_COLOR.WHITE,
          formatter: (el) => (el.data.count > 0) ? `${el.data.count}` : '',
        },
      },
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.CURRENT_LIGHT_LIGHT, currentData),
        color: CHART_COLOR.CURRENT_LIGHT,
        label: {
          show: true,
          position: 'insideRight',
          fontWeight: 'bold',
          color: CHART_COLOR.WHITE,
          formatter: (el) => (el.data.count > 0) ? `${el.data.count}` : '',
        },
      },
    ],
  };

  return options;
}
