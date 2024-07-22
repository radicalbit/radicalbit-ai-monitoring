import ReactEchartsCore from 'echarts-for-react/lib/core';
import { BarChart } from 'echarts/charts';
import {
  GridComponent,
  MarkLineComponent,
  MarkPointComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { memo } from 'react';
import chartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  BarChart,
]);

function ResidualBucketChart({ dataset, color }) {
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
      option={chartOptions(dataset, color)}
      style={{ height: '14rem' }}
    />

  );
}

export default memo(ResidualBucketChart);
