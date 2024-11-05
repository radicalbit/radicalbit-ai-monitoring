import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { numberFormatter } from '@Src/constants';
import * as commonChartOptions from '@Helpers/common-chart-options';

export default function lineChartOptions(currentDataset, referenceDataset) {
  let dataSeries = currentDataset.map((el) => {
    const currentSeries = el.data.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);
    return commonChartOptions.seriesOptions(CHART_TYPE.LINE, el.className, null, currentSeries);
  });

  const legendLabel = dataSeries.map(({ name }) => name);

  if (referenceDataset) {
    const series = referenceDataset.map((el) => {
      const referenceSeries = el.data.map(({ timestamp, value }) => [timestamp, numberFormatter().format(value)]);
      const referenceOption = {
        ...commonChartOptions.seriesOptions(CHART_TYPE.LINE, el.className, null, referenceSeries),
        endLabel: {
          show: true,
          color: CHART_COLOR.REFERENCE,
          formatter: ({ value }) => `${value[1]}`,
          backgroundColor: '#fff',
        },

      };
      referenceOption.lineStyle = {
        width: 2,
        type: 'dotted',
      };
      return referenceOption;
    });
    dataSeries = dataSeries.concat(series);
  }

  const options = {
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.TIME),
    ...commonChartOptions.gridOptions(CHART_TYPE.LINE),
    ...commonChartOptions.colorList,
    ...commonChartOptions.legendOptions(legendLabel),
    tooltip: { trigger: 'axis' },
    emphasis: { focus: 'series' },
    title: {
      text: '••• Reference',
      textStyle: {
        fontSize: 10,
        fontWeight: '300',
      },
      right: 0,
    },

    series: dataSeries,
  };

  options.grid.right = 140;
  return options;
}
