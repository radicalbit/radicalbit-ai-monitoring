import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE, CHART_COLOR } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';

export default function chartOptions(dataset, xAxisLabel, yAxisLabel, color) {
  const xsortedData = dataset.map((d) => d[0]).sort((a, b) => parseFloat(b) - parseFloat(a));
  const xMax = xsortedData[0];
  const xMin = xsortedData[xsortedData.length - 1];

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.SCATTER),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.VALUE, null, xAxisLabel),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE, null, yAxisLabel),
    tooltip: {
      axisPointer: {
        show: true,
        type: 'cross',
        lineStyle: {
          type: 'dashed',
          width: 1,
        },
      },
      valueFormatter: (value) => numberFormatter().format(value),
    },
    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.SCATTER, null, color, dataset),
      },
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.LINE, null, CHART_COLOR.RED, [[xMin, xMin], [xMax, xMax]]),
      },
    ],
  };

  options.yAxis.scale = true;
  options.xAxis.scale = true;

  return options;
}
