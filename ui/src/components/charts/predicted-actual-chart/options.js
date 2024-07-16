import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';

export default function chartOptions(dataset, xAxisLabel, yAxisLabel, color) {
  const test = [0, 27];

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
        ...commonChartOptions.seriesOptions(CHART_TYPE.LINE, null, color, test),
      },

    ],
  };

  options.yAxis.scale = false;
  options.xAxis.axisLine = {
    lineStyle: {
      width: 2,
      type: 'dashed',
    },
  };

  options.series[1].lineStyle.type = 'dotted';

  return options;
}
