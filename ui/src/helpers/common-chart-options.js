import moment from 'moment';

const dateFormatter = (value) => moment(+value).format('DD MMM HH.mm');

const xAxisCategoryType = (xAxisData) => {
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

const xAxisValueType = (xAxisData) => {
  const options = {
    xAxis: {
      type: 'value',
      boundaryGap: true,
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
    },
  };
  if (xAxisData) {
    options.xAxis.data = xAxisData;
  }
  return options;
};

const yAxisValueType = (yAxisData) => {
  const options = {
    yAxis: {
      type: 'value',
      boundaryGap: true,
      axisLabel: {
        fontSize: 9,
        color: '#9b99a1',
      },
    },
  };
  if (yAxisData) {
    options.yAxis.data = yAxisData;
  }
  return options;
};

const yAxisCategoryType = (yAxisData) => {
  const options = {
    yAxis: {
      type: 'category',
      boundaryGap: true,
      axisTick: { show: false },
      axisLine: { show: false },
      splitLine: { show: false },
      axisLabel: {
        fontSize: 9,
      },
    },
  };
  if (yAxisData) {
    options.yAxis.data = yAxisData;
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
    top: 16,
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

const colorList = {
  color: [
    '#3695D9',
    '#64A4DD',
    '#85B2E1',
    '#A2C2E5',
    '#BDD1E9',
    '#D7E1ED',
    '#F1F1F1',
    '#E3D7F1',
    '#D4BEF2',
    '#C4A5F2',
    '#B28DF2',
    '#9F74F1',
    '#8A5BF0'],
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
    lineStyle: { width: 2 },
    symbol: 'none',
  };

  if (data) {
    options.data = data;
  }

  if (color !== null) {
    options.lineStyle.color = color;
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

const barChartCommonOptions = () => ({
  emphasis: { disabled: true },
  barCategoryGap: '21%',
  barGap: '0',
  overflow: 'truncate',
  lineOverflow: 'truncate',
  itemStyle: {
    borderWidth: 1,
    borderColor: 'rgba(201, 25, 25, 1)',
  },
});

const heatmapCommonOptions = () => ({
  emphasis: { disabled: true },
});

// Object to simplify usage of common options
const yAxisOptions = (optionType, data) => {
  switch (optionType) {
    case OPTIONS_TYPE.VALUE:
      return yAxisValueType(data);
    case OPTIONS_TYPE.CATEGORY:
      return yAxisCategoryType(data);
    default:
      return false;
  }
};

const xAxisOptions = (optionType, data) => {
  switch (optionType) {
    case OPTIONS_TYPE.VALUE:
      return xAxisValueType(data);
    case OPTIONS_TYPE.CATEGORY:
      return xAxisCategoryType(data);
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
      return heatmapSeriesOptions(title, color, data);
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
  REFERENCE_LIGHT: '#DBDBDB',
  REFERENCE_DARK: '#667',
  CURRENT: '#3695d9',
  CURRENT_LIGHT: '#3795d990',
  CURRENT_DARK: '#0A71BB',
  WHITE: '#FFFFFF',
  LINE_CHART_COLOR: '#73B2E0',
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
};

export {
  yAxisOptions,
  xAxisOptions,
  seriesOptions,
  gridOptions,
  commonOptions,
  visualMapOptions,
  tooltipOptions,
  colorList,
  OPTIONS_TYPE,
  CHART_COLOR,
  CHART_TYPE,
};
