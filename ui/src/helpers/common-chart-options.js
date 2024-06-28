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
        fontSize: 10,
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
    bottom: 80,
    top: 0,
    left: 64,
    right: 0,
  },
});

const heatmapVisualMapOptions = (dataMax, colors) => {
  const options = {
    visualMap: {
      calculable: true,
      orient: 'horizontal',
      left: 'center',
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
    lineStyle: { width: 2, color },
    symbol: 'none',
  };

  if (data) {
    options.data = data;
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
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowColor: 'rgba(0, 0, 0, 0.5)',
      },
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
  overflow: 'truncate',
  lineOverflow: 'truncate',
});

const heatmapCommonOptions = () => ({
  emphasis: { disabled: true },
});

// Object to simplify usage of common options
const yAxisOptions = {
  valueType: yAxisValueType,
  categoryType: yAxisCategoryType,
};

const xAxisOptions = {
  categoryType: xAxisCategoryType,
  timeType: xAxisTimeType,
  valueType: xAxisValueType,
};

const gridOptions = {
  barChart: barGridOptions,
  lineChart: lineGridOptions,
  heatmapChart: heatmapGridOptions,
};

const seriesOptions = {
  barChart: barSeriesOptions,
  lineChart: lineSeriesOptions,
  heatmapChart: heatmapSeriesOptions,
};

const commonOptions = {
  barChart: barChartCommonOptions,
  heatmapChart: heatmapCommonOptions,
};

const visualMapOptions = {
  heatmapChart: heatmapVisualMapOptions,
};

const CHART_COLOR = {
  REFERENCE: '#9B99A1',
  REFERENCE_LIGHT: '#DBDBDB',
  REFERENCE_DARK: '#667',
  CURRENT: '#3695d9',
  CURRENT_LIGHT: '#C8E4F9',
  CURRENT_DARK: '#0A71BB',
  WHITE: '#FFFFFF',
  LINE_CHART_COLOR: '#73B2E0',
};

export {
  yAxisOptions,
  xAxisOptions,
  seriesOptions,
  gridOptions,
  commonOptions,
  visualMapOptions,
  tooltipOptions,
  CHART_COLOR,
};
