import { CHART_COLOR } from '@Container/models/Details/constants';
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

function NumericalBarChart({ dataset }) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  if (!dataset) {
    return false;
  }

  return (
    <div className="w-full h-full">
      <ReactEchartsCore
        echarts={echarts}
        onChartReady={handleOnChartReady}
        option={chartOptions(dataset, CHART_COLOR.REFERENCE)}
        scroll={{ y: '16rem' }}
      />
    </div>
  );
}

export default memo(NumericalBarChart);
