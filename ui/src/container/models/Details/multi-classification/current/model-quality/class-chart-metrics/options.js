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
    // color: [color],
    ...commonChartOptions.yAxisOptions(OPTIONS_TYPE.VALUE),
    ...commonChartOptions.xAxisOptions(OPTIONS_TYPE.TIME),
    ...commonChartOptions.gridOptions(CHART_TYPE.LINE),
    ...commonChartOptions.colorList,
    series: dataSeries,

    tooltip: {
      trigger: 'axis',
    },

    emphasis: {
      focus: 'series',
    },
    legend: {
      right: 0,
      top: 16,
      bottom: 0,
      orient: 'vertical',
      type: 'scroll',
      scrollDataIndex: 'scroll',
      pageIconSize: 8,
      pageTextStyle: {
        fontSize: 8,
      },
      data: dataSeries.map(({ name }) => name),
      textStyle: {
        fontSize: 10,
        fontWeight: '300',
      },
    },

    title: {
      text: '••• Reference',
      textStyle: {
        fontSize: 10,
        fontWeight: '300',
      },
      right: 0,
    },

  };

  options.grid.right = 140;
  return options;
}
