import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';

export default function chartOptions(dataset, referenceColor, currentColor) {
  const { length, [length - 1]: last, ...rest } = dataset.buckets.map((value) => numberFormatter().format(value));

  const values = Object.values(rest);

  const xAxisData = values.map((el, idx) => `[${el}${(idx < values.length - 1) ? `-${values[idx + 1]})` : (idx === values.length - 1) ? `-${last}]` : ''} `);

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisData),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    series: [
      commonChartOptions.seriesOptions(CHART_TYPE.BAR, 'reference', referenceColor, dataset.referenceValues),
      commonChartOptions.seriesOptions(CHART_TYPE.BAR, 'current', currentColor, dataset.currentValues),
    ],
  };

  options.xAxis.axisLabel.rotate = 20;

  return options;
}
