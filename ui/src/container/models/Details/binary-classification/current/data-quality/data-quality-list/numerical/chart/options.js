import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Container/models/Details/charts/common-chart-options';

export default function chartOptions(dataset, referenceColor, currentColor) {
  const dataFormatted = dataset.buckets.map((value) => numberFormatter().format(value));
  const lastElementData = dataFormatted.pop();
  const xAxisData = dataFormatted.map((el, idx) => `[${dataFormatted[idx]}${(idx < dataFormatted.length - 1) ? `-${dataFormatted[idx + 1]})` : (idx === dataFormatted.length - 1) ? `-${lastElementData}]` : ''} `);

  const options = {
    ...commonChartOptions.gridOptions.barChart(),
    ...commonChartOptions.xAxisOptions.categoryType(xAxisData),
    ...commonChartOptions.yAxisOptions.valueType(),
    series: [
      commonChartOptions.seriesOptions.barChart('reference', referenceColor, dataset.referenceValues),
      commonChartOptions.seriesOptions.barChart('current', currentColor, dataset.currentValues),
    ],
  };

  options.xAxis.axisLabel.rotate = 20;

  return options;
}
