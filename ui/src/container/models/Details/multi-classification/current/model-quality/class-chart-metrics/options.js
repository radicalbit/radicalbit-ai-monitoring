import * as commonChartOptions from '@Helpers/common-chart-options';
import { CHART_COLOR, CHART_TYPE, OPTIONS_TYPE } from '@Helpers/common-chart-options';
import { echartNumberFormatter } from '@Src/constants';

export default function lineChartOptions(currentDataset, referenceDataset) {
  let dataSeries = currentDataset.map((el) => {
    const currentSeries = el.data.map(({ timestamp, value }) => [timestamp, echartNumberFormatter().format(value)]);
    return commonChartOptions.seriesOptions(CHART_TYPE.LINE, el.className, null, currentSeries);
  });

  const legendLabel = dataSeries.map(({ name }) => name);
  const legendSelected = legendLabel.reduce((acc, name, idx) => ({ [name]: idx === 0, ...acc }), {});

  if (referenceDataset) {
    const series = referenceDataset.map((el) => {
      const referenceSeries = el.data.map(({ timestamp, value }) => [timestamp, echartNumberFormatter().format(value)]);
      const referenceOption = {
        ...commonChartOptions.seriesOptions(CHART_TYPE.LINE, el.className, null, referenceSeries),
        endLabel: {
          show: true,
          color: CHART_COLOR.REFERENCE_LIGHT,
          formatter: ({ value }) => `${value[1]}`,
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
    ...commonChartOptions.legendOptions(legendLabel, legendSelected),
    tooltip: { trigger: 'axis' },
    emphasis: { focus: 'series' },
    title: {
      text: '••• Reference',
      textStyle: {
        fontSize: 10,
        fontWeight: '300',
        color: CHART_COLOR.REFERENCE_LIGHT,
      },
      right: 0,
    },

    series: dataSeries,
  };

  options.grid.right = 140;
  return options;
}
