import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function chartOptions(title, referenceDataset, currentDataset) {
  const xAxisLabel = currentDataset.map(({ name }) => name);

  const referenceData = referenceDataset.map(({ count, percentage }) => ({ percentage, count, value: count }));
  const currentData = currentDataset.map(({ count, percentage }) => ({ percentage, count, value: count }));

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisLabel),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),

    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
        color: CHART_COLOR.REFERENCE_LIGHT,
        label: {
          show: true,
          position: 'top',
          fontWeight: 'bold',
          rotate: 45,
          offset: [25, 5],
          color: CHART_COLOR.REFERENCE_DARK,
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, `${title}_current`, CHART_COLOR.CURRENT_LIGHT, currentData),
        color: CHART_COLOR.CURRENT_LIGHT,
        label: {
          show: true,
          position: 'top',
          fontWeight: 'bold',
          rotate: 45,
          offset: [25, 5],
          color: CHART_COLOR.CURRENT_DARK,
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
    ],
  };

  options.grid.top = 25;
  options.xAxis.axisLabel.rotate = 35;

  return options;
}
