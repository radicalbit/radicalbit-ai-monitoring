import ReactEchartsCore from 'echarts-for-react/lib/core';
import {
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  TooltipComponent,
} from 'echarts/components';
import { PieChart as PieChartEchart } from 'echarts/charts';
import * as echarts from 'echarts/lib/echarts';

import pieChartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  LegendComponent,
  PieChartEchart,
  TooltipComponent,
]);

function PieChart({ title, data }) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  const splittedTitle = title.split(' ');
  const currentData = parseFloat(data).toFixed(4) * 100;
  const referenceData = (1 - parseFloat(data).toFixed(4)) * 100;

  return (
    <div className="flex flex-row items-center gap-2">
      <ReactEchartsCore
        echarts={echarts}
        onChartReady={handleOnChartReady}
        option={pieChartOptions({ currentData, referenceData })}
        style={{ height: '8rem', width: '100%' }}
      />

      <div className="flex flex-col items-start justify-center">
        <p className="font-bold text-3xl" style={{ marginBottom: '-0.6rem' }}>{splittedTitle[0]}</p>

        <p className="m-0 text-2xl tracking-wider">{splittedTitle[1]}</p>
      </div>
    </div>
  );
}

export default PieChart;
