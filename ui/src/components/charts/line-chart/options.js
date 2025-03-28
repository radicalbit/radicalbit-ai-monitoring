import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';

export default function lineChartOptions(title, color, currentDataset, referenceDataset) {
  const currentDatasetFormatted = currentDataset.map(({ timestamp, value }) => [
    timestamp,
    (value > 1000)
      ? Number.parseFloat(value).toExponential(2)
      : numberFormatter().format(value),
  ]);

  const series = [
    commonChartOptions.seriesOptions(CHART_TYPE.LINE, title, CHART_COLOR.LINE_CHART_COLOR, currentDatasetFormatted),
  ];

  if (referenceDataset) {
    const referenceDatasetFormatted = referenceDataset.map(({ timestamp, value }) => [timestamp, (value > 1000) ? Number.parseFloat(value).toExponential(2) : numberFormatter().format(value)]);

    const referenceLine = {
      ...commonChartOptions.seriesOptions(CHART_TYPE.LINE, 'Reference', CHART_COLOR.REFERENCE, referenceDatasetFormatted),
      endLabel: {
        show: true,
        color: CHART_COLOR.REFERENCE_LIGHT,
        formatter: ({ value }) => `${value[1]}`,
      },
      color: CHART_COLOR.REFERENCE_LIGHT,
    };

    referenceLine.lineStyle.type = 'dotted';
    series.push(referenceLine);
  }

  const options = {

    color: [color],
    ...commonChartOptions.tooltipOptions(),
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.TIME),
    ...commonChartOptions.gridOptions(CHART_TYPE.LINE),
    series,
    legend: {
      show: true,
      textStyle: {
        color: CHART_COLOR.REFERENCE_LIGHT,
      },
      right: 0,
    },
  };

  options.xAxis.scale = true;
  options.yAxis.scale = true;
  return options;
}
