import { CHART_COLOR } from '@Helpers/common-chart-options';
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

function WordBarChart({ dataset }) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  if (!dataset) {
    return false;
  }

  return (
    <div className="w-full h-full shadow overflow-auto max-w-full">
      <ReactEchartsCore
        echarts={echarts}
        onChartReady={handleOnChartReady}
        option={chartOptions(dataset, CHART_COLOR.REFERENCE, CHART_COLOR.CURRENT)}
        style={{ height: '15rem', width: '100%' }}
      />
    </div>
  );
}

export default memo(WordBarChart);
