import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { echartNumberFormatter } from '@Src/constants';

export default function chartOptions(dataset, barChartSelectedIndex) {
  const xAxisData = dataset.probs.map(({ token }) => token);

  const seriesData = dataset.probs.map(({ prob }) => echartNumberFormatter().format(prob));

  const barChartChangeColorFn = (p) => p.data <= 0.33 ? 'rgb(240,0,0)' : p.data > 0.33 && p.data <= 0.66 ? 'rgb(251,228,5)' : 'rgb(77,182,148)';

  const options = {
    ...commonChartOptions.tooltipOptions(),
    ...commonChartOptions.gridOptions(CHART_TYPE.BAR),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, xAxisData),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE, undefined, 'Probabilty'),
    ...commonChartOptions.commonOptions(CHART_TYPE.BAR),
    selectedMode: 'single',
    series: [
      commonChartOptions.seriesOptions(CHART_TYPE.BAR, undefined, barChartChangeColorFn, seriesData),
    ],
  };

  if (barChartSelectedIndex >= 0) {
    options.series[0].markArea = {
      itemStyle: {
        color: commonChartOptions.CHART_COLOR.REFERENCE_LIGHT,
      },
      data: [
        [{ xAxis: barChartSelectedIndex }, { xAxis: barChartSelectedIndex }],
      ],
    };
  }

  options.xAxis.axisLabel.rotate = 65;
  options.barCategoryGap = '1';

  options.emphasis = { disabled: false };
  options.barWidth = 18;

  options.grid.left = 20;
  options.grid.bottom = 40;

  const endValue = Math.min(Math.floor(dataset.length / 10), 50);
  options.dataZoom = commonChartOptions.dataZoomOptions({ endValue });
  options.dataZoom[0].minSpan = 5;
  options.dataZoom[0].maxSpan = 5;

  options.animation = false;

  return options;
}
