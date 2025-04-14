import ReactEchartsCore from 'echarts-for-react/lib/core';
import { PieChart as PieChartEchart } from 'echarts/charts';
import {
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  TooltipComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';

import { echartNumberFormatter } from '@Src/constants';
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
  const currentData = echartNumberFormatter({ maximumSignificantDigits: 4 }).format(data * 100);

  if (data <= 0) {
    return (
      <div className="flex flex-row items-center">
        <EmptyPieChart />

        <Label percentage={0} title={title} />

      </div>
    );
  }

  return (
    <div className="flex flex-row items-center">
      <EvaluatedPieChart data={data} />

      <Label percentage={currentData} title={title} />
    </div>
  );
}

function EmptyPieChart() {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  return (
    <ReactEchartsCore
      echarts={echarts}
      onChartReady={handleOnChartReady}
      option={pieChartOptions({ currentData: 0, referenceData: 100 })}
      style={{ height: '8rem', width: '10rem' }}
    />
  );
}

function EvaluatedPieChart({ data }) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  const currentData = echartNumberFormatter({ maximumSignificantDigits: 4 }).format(data * 100);
  const referenceData = echartNumberFormatter({ maximumSignificantDigits: 4 }).format((1 - data) * 100);
  return (
    <ReactEchartsCore
      echarts={echarts}
      onChartReady={handleOnChartReady}
      option={pieChartOptions({ currentData, referenceData })}
      style={{ height: '8rem', width: '10rem' }}
    />
  );
}

function Label({ title, percentage }) {
  return (
    <div className="flex flex-col items-start justify-center w-full">
      <h1 className="font-bold text-3xl" style={{ marginBottom: '-0.25rem' }}>
        {percentage}

        <small className="font-normal">%</small>
      </h1>

      <h2 className="m-0 text-lg font-normal">{title}</h2>
    </div>
  );
}

export default PieChart;
