import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';

export default function chartOptions(title, dataset) {
  const xAxisLabel = dataset?.map(({ name }) => name);

  const referenceData = dataset?.map(({ count, percentage }) => ({ percentage, count, value: percentage }));

  const options = {
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisLabel),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.PERCENTAGE),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),
    tooltip: {
      ...commonChartOptions.tooltipOptions(CHART_TYPE.BAR),
      formatter: (params) => {
        console.debug(params);
        return `
          ${params.marker} Name: ${params.name}<br/> Count: ${params.data.count}
        `;
      },
    },
    series: [
      {
        ...commonChartOptions.seriesOptions(CHART_TYPE.BAR, title, CHART_COLOR.REFERENCE_LIGHT, referenceData),
      },
    ],
  };

  if (referenceData.length >= 30) {
    const endValue = Math.min(Math.floor(referenceData.length / 10), 50);

    options.dataZoom = commonChartOptions.dataZoomOptions({ endValue });
    options.grid.bottom = 40;
  }

  options.grid.top = 25;
  options.xAxis.axisLabel.rotate = 35;

  return options;
}
