import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function chartOptions(title, dataset) {
  const yAxisLabel = dataset?.map(({ name }) => name);

  const referenceData = dataset?.map(({ count, percentage }) => ({ percentage, count, value: count }));

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.CATEGORY, yAxisLabel),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),
    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
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

  return options;
}
