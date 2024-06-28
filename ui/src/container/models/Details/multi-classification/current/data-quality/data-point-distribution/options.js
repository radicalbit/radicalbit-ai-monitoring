import { CHART_COLOR } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function chartOptions(title, referenceDataset, currentDataset) {
  const yAxisLabel = currentDataset.map(({ name }) => name);

  const referenceData = referenceDataset.map(({ count, percentage }) => ({ percentage, count, value: count }));
  const currentData = currentDataset.map(({ count, percentage }) => ({ percentage, count, value: count }));

  const options = {
    ...commonChartOptions.gridOptions.barChart(),
    ...commonChartOptions.xAxisOptions.valueType(),
    ...commonChartOptions.yAxisOptions.categoryType(yAxisLabel),
    ...commonChartOptions.commonOptions.barChart(),
    series: [
      {
        ...commonChartOptions.seriesOptions.barChart(title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
        color: CHART_COLOR.REFERENCE_LIGHT,
        label: {
          show: true,
          position: 'insideRight',
          fontWeight: 'bold',
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
      {
        ...commonChartOptions.seriesOptions.barChart(title, CHART_COLOR.CURRENT_LIGHT_LIGHT, currentData),
        color: CHART_COLOR.CURRENT_LIGHT,
        label: {
          show: true,
          position: 'insideRight',
          fontWeight: 'bold',
          color: CHART_COLOR.CURRENT_DARK,
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
    ],
  };

  return options;
}
