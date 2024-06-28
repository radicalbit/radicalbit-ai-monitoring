import * as commonChartOptions from '@Helpers/common-chart-options';

export default function confusionMatrixOptions(dataset, labelClass, colors) {
  let dataMax = 0;
  const heatmapData = dataset.toReversed().reduce((accumulator, datas, yIndex) => accumulator.concat(datas.map((data, xIndex) => {
    if (data > dataMax) {
      dataMax = data;
    }
    return [xIndex, yIndex, data];
  })), []);

  const options = {
    ...commonChartOptions.yAxisOptions.categoryType(labelClass.yAxisLabel),
    ...commonChartOptions.xAxisOptions.categoryType(labelClass.xAxisLabel),
    ...commonChartOptions.gridOptions.heatmapChart(),
    ...commonChartOptions.commonOptions.heatmapChart(),
    ...commonChartOptions.visualMapOptions.heatmapChart(dataMax, colors),
    series: {
      ...commonChartOptions.seriesOptions.heatmapChart(heatmapData),
    },
  };

  return options;
}
