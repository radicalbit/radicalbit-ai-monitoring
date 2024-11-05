import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';

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
      },
    ],
  };

  if (referenceData.length >= 30) {
    options.dataZoom = commonChartOptions.dataZoomOptions();
    options.grid.bottom = 40;
  }

  options.grid.top = 25;
  options.xAxis.axisLabel.rotate = 35;

  return options;
}
