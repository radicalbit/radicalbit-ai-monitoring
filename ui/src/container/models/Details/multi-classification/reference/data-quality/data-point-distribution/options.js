import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function chartOptions(title, dataset) {
  const xAxisLabel = dataset?.map(({ name }) => name);

  const referenceData = dataset?.map(({ count, percentage }) => ({ percentage, count, value: count }));

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisLabel),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),
    ...commonChartOptions.tooltipOptions(CHART_TYPE.BAR),
    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
        color: CHART_COLOR.REFERENCE_LIGHT,
        label: {
          show: false,
          position: 'top',
          fontWeight: 'bold',
          rotate: 45,
          offset: [25, 5],
          formatter: (el) => (el.data.count > 0) ? `${el.data.count} (${numberFormatter().format(el.data.percentage)}%)` : '',
        },
      },
    ],
  };

  if (referenceData.length >= 30) {
    options.dataZoom = [
      {
        show: true,
      },
      {
        type: 'inside',
      },
    ];
    options.grid.bottom = 40;
  }

  options.grid.top = 25;
  options.xAxis.axisLabel.rotate = 35;

  return options;
}
