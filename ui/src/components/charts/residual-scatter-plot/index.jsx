import ReactEchartsCore from 'echarts-for-react/lib/core';
import { ScatterChart } from 'echarts/charts';
import {
  GridComponent,
  MarkLineComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { memo } from 'react';
import chartOptions from './options';

echarts.use([
  GridComponent,
  ScatterChart,
  MarkLineComponent,
]);

function ResidualScatterPlot({
  dataset, xAxisLabel, yAxisLabel, color,
}) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  if (!dataset) {
    return false;
  }

  return (
    <ReactEchartsCore
      echarts={echarts}
      onChartReady={handleOnChartReady}
      option={chartOptions(dataset, xAxisLabel, yAxisLabel, color)}
      style={{ height: '48rem', width: '100%' }}
    />

  );
}

export default memo(ResidualScatterPlot);
