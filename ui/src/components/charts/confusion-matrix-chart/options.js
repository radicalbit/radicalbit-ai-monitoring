import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';

export default function confusionMatrixOptions(dataset, labelClass, colors) {
  let dataMax = 0;
  const heatmapData = dataset.toReversed().reduce((accumulator, datas, yIndex) => accumulator.concat(datas.map((data, xIndex) => {
    if (data > dataMax) {
      dataMax = data;
    }
    return [xIndex, yIndex, data];
  })), []);

  const options = {
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.CATEGORY, labelClass.yAxisLabel, 'Actual'),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.CATEGORY, labelClass.xAxisLabel, 'Predicted'),
    ...commonChartOptions.gridOptions(CHART_TYPE.HEATMAP),
    ...commonChartOptions.commonOptions(CHART_TYPE.HEATMAP),
    ...commonChartOptions.visualMapOptions(CHART_TYPE.HEATMAP, dataMax, colors, '250rem'),
    series: {
      ...commonChartOptions.seriesOptions(CHART_TYPE.HEATMAP, null, null, heatmapData),
    },
  };

  options.xAxis.axisLabel.rotate = 45;
  options.grid.bottom = 60;
  return options;
}
