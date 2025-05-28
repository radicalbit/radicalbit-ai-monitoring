import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
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
    ...commonChartOptions.tooltipOptions(CHART_TYPE.BAR),

    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
      },
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, `${title}_current`, CHART_COLOR.CURRENT_LIGHT, currentData),
      },
    ],
  };

  if (currentData.length >= 20 || referenceData.length >= 20) {
    const endValue = Math.min(Math.floor(referenceData.length / 10), 50);

    options.dataZoom = commonChartOptions.dataZoomOptions({ endValue });
    options.grid.bottom = 40;
  }

  options.grid.top = 25;
  options.xAxis.axisLabel.rotate = 35;

  return options;
}
