import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';

export default function chartOptions(dataset) {
  const xAxisData = dataset.probs.map(({ token }) => token);

  const seriesData = dataset.probs.map(({ prob }) => numberFormatter().format(prob));

  const options = {
    ...commonChartOptions.tooltipOptions(),
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisData),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),
    series: [
      commonChartOptions.seriesOptions(CHART_TYPE.BAR, 'Probability', commonChartOptions.CHART_COLOR.CURRENT, seriesData),
    ],
  };

  options.xAxis.axisLabel.rotate = 20;
  options.barCategoryGap = '1';

  options.dataZoom = commonChartOptions.dataZoomOptions();

  options.grid.bottom = 40;
  options.barWidth = 30;
  options.dataZoom[0].minSpan = 4;
  options.dataZoom[0].maxSpan = 4;

  return options;
}
