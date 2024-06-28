import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function chartOptions(dataset, color) {
  const { length, [length - 1]: last, ...rest } = dataset.buckets.map((value) => numberFormatter().format(value));

  const values = Object.values(rest);

  const xAxisData = values.map((el, idx) => `[${el}${(idx < values.length - 1) ? `-${values[idx + 1]})` : (idx === values.length - 1) ? `-${last}]` : ''} `);

  const options = {
    ...commonChartOptions.gridOptions.barChart(),
    ...commonChartOptions.xAxisOptions.categoryType(xAxisData),
    ...commonChartOptions.yAxisOptions.valueType(),
    series: [
      commonChartOptions.seriesOptions.barChart('reference', color, dataset.referenceValues),
    ],
  };

  options.xAxis.axisLabel.rotate = 20;

  return options;
}
