import { numberFormatter } from '@Src/constants';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function lineChartOptions(color, currentDataset, referenceDataset) {
  console.debug('🚀 ~ lineChartOptions ~ referenceDataset:', referenceDataset);
  let dataSeries = currentDataset.map((el) => {
    const currentSeries = el.data.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);
    return commonChartOptions.seriesOptions.lineChart(el.className, null, currentSeries);
  });

  if (referenceDataset) {
    const series = referenceDataset.map((el) => {
      const referenceSeries = el.data.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);
      const referenceOption = {
        ...commonChartOptions.seriesOptions.lineChart(el.className, null, referenceSeries),
        endLabel: {
          show: true,
          color: CHART_COLOR.REFERENCE,
          formatter: ({ value }) => `${value[1]}`,
        },
      };
      referenceOption.lineStyle.type = 'dotted';
      return referenceOption;
    });
    dataSeries = dataSeries.concat(series);
  }

  const options = {
    // color: [color],
    ...commonChartOptions.yAxisOptions.valueType(),
    ...commonChartOptions.xAxisOptions.timeType(),
    ...commonChartOptions.gridOptions.lineChart(),
    ...commonChartOptions.tooltipOptions(),
    series: dataSeries,
    legend: {
      right: 0,
      orient: 'vertical',
      data: dataSeries.map(({ name }) => name),
    },
  };

  options.grid.right = 140;
  return options;
}
