import moment from 'moment';

const dateFormatter = (value) => moment(+value).format('DD MMM HH.mm');

const xAxisCategoryType = (xAxisData, xAxisName) => {
  const options = {
    xAxis: {
      type: 'category',
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: { show: false },
      axisLabel: {
        fontSize: 12,
        interval: 0,
        color: '#9b99a1',
      },
    },
  };
  if (xAxisData) {
    options.xAxis.data = xAxisData;
  }

  if (xAxisName) {
    options.xAxis.name = xAxisName;
    options.xAxis.nameGap = 25;
    options.xAxis.nameLocation = 'middle';
  }
  return options;
};

const xAxisTimeType = (xAxisData) => {
  const options = {
    xAxis: {
      type: 'time',
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: { show: false },
      axisLabel: {
        formatter: dateFormatter,
        fontSize: 12,
        color: '#9b99a1',
      },
    },
  };
  if (xAxisData) {
    options.xAxis.data = xAxisData;
  }
  return options;
};

const xAxisValueType = (xAxisData, xAxisName) => {
  const options = {
    xAxis: {
      type: 'value',
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
      splitLine: {
        lineStyle: {
          color: '#9f9f9f54',
        },
      },
    },
  };

  if (xAxisData) {
    options.xAxis.data = xAxisData;
  }

  if (xAxisName) {
    options.xAxis.name = xAxisName;
    options.xAxis.nameGap = 25;
    options.xAxis.nameLocation = 'middle';
  }
  return options;
};

const yAxisValueType = (yAxisData, yAxisName) => {
  const options = {
    yAxis: {
      type: 'value',
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
      splitLine: {
        lineStyle: {
          color: '#9f9f9f54',
        },
      },
    },
  };
  if (yAxisData) {
    options.yAxis.data = yAxisData;
  }

  if (yAxisName) {
    options.yAxis.name = yAxisName;
    options.yAxis.nameGap = 25;
    options.yAxis.nameLocation = 'middle';
  }
  return options;
};

const yAxisCategoryType = (yAxisData, yAxisName) => {
  const options = {
    yAxis: {
      type: 'category',
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: { show: false },
      axisLabel: {
        fontSize: 12,
        color: CHART_COLOR.REFERENCE_LIGHT,
      },
    },
  };
  if (yAxisData) {
    options.yAxis.data = yAxisData;
  }

  if (yAxisName) {
    options.yAxis.name = yAxisName;
    options.yAxis.nameGap = 25;
    options.yAxis.nameLocation = 'middle';
  }
  return options;
};

const barGridOptions = () => ({
  grid: {
    left: 0,
    right: 20,
    bottom: 0,
    top: 10,
    containLabel: true,
  },
});

const lineGridOptions = () => ({
  grid: {
    bottom: 0,
    top: 32,
    left: 0,
    right: 64,
    containLabel: true,
  },
});

const heatmapGridOptions = () => ({
  grid: {
    bottom: 24,
    top: 0,
    left: 64,
    right: 60,
  },
});

const scatterGridOptions = () => ({
  grid: {
    left: 20,
    right: 0,
    bottom: 50,
    top: 24,
    containLabel: true,
  },
});

const heatmapVisualMapOptions = (dataMax, colors, itemHeight) => {
  const options = {
    visualMap: {
      calculable: true,
      orient: 'vertical',
      right: 'right',
      top: 'center',
      itemHeight,
    },
  };

  if (dataMax) {
    options.visualMap.max = dataMax;
  }

  if (colors) {
    options.visualMap.inRange = { color: colors };
  }

  return options;
};

const tooltipOptions = () => ({
  tooltip: {
    trigger: 'axis',
    crosshairs: true,
    axisPointer: {
      type: 'cross',
      label: {
        show: true,
      },
    },
  },
});

const dataZoomOptions = ({ endValue = 0 }) => ([
  {
    type: 'slider',
    show: true,
    xAxisIndex: 0,
    startValue: 0,
    endValue,
  },
  {
    type: 'inside',
  },
]);

const legendOptions = (data, legendSelected) => {
  const options = {
    legend: {
      right: 0,
      top: 16,
      bottom: 0,
      orient: 'vertical',
      type: 'scroll',
      scrollDataIndex: 'scroll',
      pageIconSize: 8,
      pageTextStyle: {
        fontSize: 9,
        color: '#9b99a1',
      },
      textStyle: {
        fontSize: 9,
        color: CHART_COLOR.REFERENCE_LIGHT,
        fontWeight: '300',
      },
    },
  };

  if (data) {
    options.legend.data = data;
  }

  if (legendSelected) {
    options.legend.selected = legendSelected;
  }

  return options;
};

const barSeriesOptions = (title, color, data) => {
  const options = {
    title,
    type: 'bar',
    itemStyle: { color },
  };

  if (data) {
    options.data = data;
  }

  return options;
};

const lineSeriesOptions = (title, color, data) => {
  const options = {
    name: title,
    type: 'line',
    lineStyle: { width: 2.2 },
    symbol: 'none',
  };

  if (data) {
    options.data = data;
  }

  if (color !== null) {
    options.lineStyle.color = color;
    options.itemStyle = { color };
  }

  return options;
};

const heatmapSeriesOptions = (data) => {
  const options = {
    name: '',
    type: 'heatmap',
    label: {
      show: true,
    },
  };

  if (data) {
    options.data = data;
  }

  return options;
};

const scatterSeriesOptions = (data, color) => {
  const options = {
    name: '',
    type: 'scatter',
    emphasis: {
      focus: 'series',
    },
    color,
  };

  if (data) {
    options.data = data;
  }

  return options;
};

const barChartCommonOptions = () => ({
  emphasis: { disabled: true },
  barCategoryGap: '21%',
  barGap: '0',
  itemStyle: {
    borderWidth: 1,
    borderColor: 'rgba(201, 25, 25, 1)',
  },
});

const heatmapCommonOptions = () => ({
  emphasis: { disabled: true },
  axis: {
    axisLabel: { // tbd
      fontSize: 9,
      color: '#9b99a1',
    },
  },
});

// Object to simplify usage of common options
const yAxisOptions = (optionType, data, yAxisName) => {
  switch (optionType) {
    case OPTIONS_TYPE.VALUE:
      return yAxisValueType(data, yAxisName);
    case OPTIONS_TYPE.CATEGORY:
      return yAxisCategoryType(data, yAxisName);
    default:
      return false;
  }
};

const xAxisOptions = (optionType, data, xAxisName) => {
  switch (optionType) {
    case OPTIONS_TYPE.VALUE:
      return xAxisValueType(data, xAxisName);
    case OPTIONS_TYPE.CATEGORY:
      return xAxisCategoryType(data, xAxisName);
    case OPTIONS_TYPE.TIME:
      return xAxisTimeType(data);
    default:
      return false;
  }
};

const gridOptions = (chartType) => {
  switch (chartType) {
    case CHART_TYPE.BAR:
      return barGridOptions();
    case CHART_TYPE.LINE:
      return lineGridOptions();
    case CHART_TYPE.HEATMAP:
      return heatmapGridOptions();
    case CHART_TYPE.SCATTER:
      return scatterGridOptions();
    default:
      return false;
  }
};

const seriesOptions = (chartType, title, color, data) => {
  switch (chartType) {
    case CHART_TYPE.BAR:
      return barSeriesOptions(title, color, data);
    case CHART_TYPE.LINE:
      return lineSeriesOptions(title, color, data);
    case CHART_TYPE.HEATMAP:
      return heatmapSeriesOptions(data);
    case CHART_TYPE.SCATTER:
      return scatterSeriesOptions(data, color);
    default:
      return false;
  }
};

const commonOptions = (chartType) => {
  switch (chartType) {
    case CHART_TYPE.BAR:
      return barChartCommonOptions();
    case CHART_TYPE.HEATMAP:
      return heatmapCommonOptions();
    default:
      return false;
  }
};

const visualMapOptions = (chartType, dataMax, colors, itemHeight) => {
  switch (chartType) {
    case CHART_TYPE.HEATMAP:
      return heatmapVisualMapOptions(dataMax, colors, itemHeight);
    default:
      return false;
  }
};

const CHART_COLOR = {
  REFERENCE: '#9B99A1',
  REFERENCE_LIGHT: '#9B99A1',
  REFERENCE_DARK: '#667',
  CURRENT: '#3695d9',
  CURRENT_LIGHT: '#3695d9',
  CURRENT_DARK: '#0A71BB',
  WHITE: '#FFFFFF',
  LINE_CHART_COLOR: '#73B2E0',
  RED: '#ff0000',
  REGRESSION_LINE: '#8D6ECF',
  DIAGONAL_LINE: '#FFC000',
};

const OPTIONS_TYPE = {
  CATEGORY: 'CATEGORY',
  TIME: 'TIME',
  VALUE: 'VALUE',
};

const CHART_TYPE = {
  BAR: 'bar',
  HEATMAP: 'heatmap',
  LINE: 'line',
  SCATTER: 'scatter',
};

const colorList = {
  color: [
    '#00BFFF',
    '#1E90FF',
    '#00CED1',
    '#20B2AA',
    '#4169E1',
    '#6A5ACD',
    '#8A2BE2',
    '#9400D3',
    '#BA55D3',
  ],
};

export {
  CHART_COLOR,
  CHART_TYPE, colorList, commonOptions, dataZoomOptions, gridOptions, legendOptions, OPTIONS_TYPE, seriesOptions, tooltipOptions, visualMapOptions, xAxisOptions, yAxisOptions,
};
