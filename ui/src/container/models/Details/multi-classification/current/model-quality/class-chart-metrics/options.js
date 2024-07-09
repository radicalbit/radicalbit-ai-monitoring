import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function lineChartOptions(color, currentDataset, referenceDataset) {
  let dataSeries = currentDataset.map((el) => {
    const currentSeries = el.data.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);
    return commonChartOptions.seriesOptions(CHART_TYPE.LINE, el.className, null, currentSeries);
  });

  if (referenceDataset) {
    const series = referenceDataset.map((el) => {
      const referenceSeries = el.data.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);
      const referenceOption = {
        ...commonChartOptions.seriesOptions(CHART_TYPE.LINE, el.className, null, referenceSeries),
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
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.TIME),
    ...commonChartOptions.gridOptions(CHART_TYPE.LINE),
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
