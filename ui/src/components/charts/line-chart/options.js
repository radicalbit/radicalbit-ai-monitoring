import { numberFormatter } from '@Src/constants';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function lineChartOptions(title, color, currentDataset, referenceDataset) {
  const currentDatasetFormatted = currentDataset.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);

  const series = [
    commonChartOptions.seriesOptions.lineChart(title, CHART_COLOR.LINE_CHART_COLOR, currentDatasetFormatted),
  ];

  if (referenceDataset) {
    const referenceDatasetFormatted = referenceDataset.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);

    const referenceLine = {
      ...commonChartOptions.seriesOptions.lineChart('Reference', CHART_COLOR.REFERENCE, referenceDatasetFormatted),
      endLabel: {
        show: true,
        color: CHART_COLOR.REFERENCE,
        formatter: ({ value }) => `Reference\n${value[1]}`,
      },
      color: CHART_COLOR.REFERENCE,
    };

    referenceLine.lineStyle.type = 'dotted';
    series.push(referenceLine);
  }

  return {
    color: [color],
    ...commonChartOptions.tooltipOptions(),
    ...commonChartOptions.yAxisOptions.valueType(),
    ...commonChartOptions.xAxisOptions.timeType(),
    ...commonChartOptions.gridOptions.lineChart(),
    series,
  };
}
