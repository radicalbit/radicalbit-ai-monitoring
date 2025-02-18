import ReactEchartsCore from 'echarts-for-react/lib/core';
import { BarChart } from 'echarts/charts';
import {
  GridComponent,
  MarkAreaComponent,
  MarkLineComponent,
  MarkPointComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { memo, useEffect, useState } from 'react';
import chartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  BarChart,
  MarkAreaComponent,
]);

function WordBarChart({ dataset, barChartSelectedIndex }) {
  const [echartRef, setEchartRef] = useState(null);
  const [options, setOptions] = useState(chartOptions(dataset, barChartSelectedIndex));

  const handleOnChartReady = (echart) => {
    setTimeout(echart.resize);
  };

  useEffect(() => {
    setOptions(chartOptions(dataset, barChartSelectedIndex));

    if (echartRef && barChartSelectedIndex >= 0) {
      const action = {
        type: 'dataZoom',
        dataZoomIndex: 0,
        start: ((barChartSelectedIndex / dataset.probs.length) * 100) - 2,
      };

      echartRef.getEchartsInstance().dispatchAction(action);
    }
  }, [barChartSelectedIndex, dataset, echartRef]);

  if (!dataset) {
    return false;
  }

  return (
    <div className="w-full h-full shadow overflow-auto max-w-full">

      <ReactEchartsCore
        echarts={echarts}
        onChartReady={handleOnChartReady}
        option={options}
        ref={(e) => setEchartRef(e)}
        style={{ height: '15rem', width: '100%' }}
      />
    </div>
  );
}

export default memo(WordBarChart);
