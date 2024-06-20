export default function confusionMatrixOptions(dataset, labelClass, colors) {
  let dataMax = 0;
  const heatMapData = dataset.toReversed().reduce((accumulator, datas, yIndex) => accumulator.concat(datas.map((data, xIndex) => {
    if (data > dataMax) {
      dataMax = data;
    }
    return [xIndex, yIndex, data];
  })), []);

  return {
    yAxis: [
      {
        type: 'category',
        data: labelClass.yAxisLabel,
      },
    ],
    xAxis: [
      {
        type: 'category',
        splitLine: {
          show: false,
        },
        data: labelClass.xAxisLabel,
      },
    ],
    grid: {
      bottom: 80,
      top: 0,
      left: 64,
      right: 0,
    },
    visualMap: {
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      inRange: {
        color: colors,
      },
      max: dataMax,
    },
    series: [
      {
        name: '',
        type: 'heatmap',
        data: heatMapData,
        label: {
          show: true,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };
}
