import { CHART_COLOR } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function chartOptions(title, dataset) {
  const xAxisLabel = dataset.map(({ name }) => name);

  const referenceData = dataset.map(({ count, percentage }) => ({ percentage, count, value: count }));

  const options = {
    ...commonChartOptions.gridOptions.barChart(),
    xAxis: commonChartOptions.xAxisOptions.categoryType(xAxisLabel).xAxis,
    yAxis: commonChartOptions.yAxisOptions.valueType().yAxis,
    ...commonChartOptions.commonOptions.barChart(),
    series: [
      {
        ...commonChartOptions.seriesOptions.barChart(title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
        color: CHART_COLOR.REFERENCE_LIGHT,
        label: {
          show: true,
          position: 'top',
          fontWeight: 'bold',
          rotate: 45,
          offset: [25, 5],
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
    ],
  };
  options.grid.top = 25;
  options.xAxis.axisLabel.rotate = 35;

  return options;
}
