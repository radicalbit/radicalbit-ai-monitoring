import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';

export default function chartOptions(dataset, referenceColor, currentColor) {
  const { length, [length - 1]: last, ...rest } = dataset.buckets.map((value) => numberFormatter().format(value));

  const values = Object.values(rest);

  const xAxisData = values.map((el, idx) => `[${el}${(idx < values.length - 1) ? `-${values[idx + 1]})` : (idx === values.length - 1) ? `-${last}]` : ''} `);

  const combinedReference = dataset.referenceValues.map((count, index) => ({
    count,
    percentage: dataset.referenceValuesPercentage[index],
    value: dataset.referenceValuesPercentage[index],
  }));

  const combinedCurrent = dataset.currentValues.map((count, index) => ({
    count,
    percentage: dataset.currentValuesPercentage[index],
    value: dataset.currentValuesPercentage[index],
  }));

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisData),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.PERCENTAGE),
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
      commonChartOptions.seriesOptions(CHART_TYPE.BAR, 'reference', referenceColor, combinedReference),
      commonChartOptions.seriesOptions(CHART_TYPE.BAR, 'current', currentColor, combinedCurrent),
    ],
  };

  options.xAxis.axisLabel.rotate = 20;

  return options;
}
