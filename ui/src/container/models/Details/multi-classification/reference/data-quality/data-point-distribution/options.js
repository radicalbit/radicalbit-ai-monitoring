import { CHART_COLOR } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';
import { ModelTypeEnum } from '@Src/store/state/models/constants';

export default function chartOptions(title, dataset, type) {
  const yAxisLabel = dataset.map(({ name }) => name);

  const referenceData = dataset.map(({ count, percentage }) => ({ percentage, count, value: count }));

  const binaryoptions = {
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
    ],
  };

  const multiClassificationOptions = {
    ...commonChartOptions.gridOptions.barChart(),
    ...commonChartOptions.xAxisOptions.categoryType(),
    ...commonChartOptions.yAxisOptions.valueType(),
    ...commonChartOptions.commonOptions.barChart(),
    tooltip: {
      formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
    },
    series: [
      {
        ...commonChartOptions.seriesOptions.barChart(title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
        color: CHART_COLOR.REFERENCE_LIGHT,
        label: {
          show: false,
          position: 'insideRight',
          fontWeight: 'bold',
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
    ],
  };

  switch (type) {
    case ModelTypeEnum.MULTI_CLASSIFICATION:
      return multiClassificationOptions;
    case ModelTypeEnum.BINARY_CLASSIFICATION:
    default:
      return binaryoptions;
  }
}
