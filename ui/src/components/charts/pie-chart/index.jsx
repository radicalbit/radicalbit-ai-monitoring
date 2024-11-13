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

import { numberFormatter } from '@Src/constants';
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
  const splittedTitle = title.split(' ');

  if (data <= 0) {
    return (
      <div className="flex flex-row items-center gap-2">
        <EmptyPieChart />

        <Label splittedTitle={splittedTitle} />
      </div>
    );
  }

  return (
    <div className="flex flex-row items-center gap-2">
      <EvaluatedPieChart data={data} />

      <Label splittedTitle={splittedTitle} />
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
      style={{ height: '8rem', width: '100%' }}
    />
  );
}

function EvaluatedPieChart({ data }) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  const currentData = numberFormatter({ maximumSignificantDigits: 4 }).format(data * 100);
  const referenceData = numberFormatter({ maximumSignificantDigits: 4 }).format((1 - data) * 100);
  return (
    <ReactEchartsCore
      echarts={echarts}
      onChartReady={handleOnChartReady}
      option={pieChartOptions({ currentData, referenceData })}
      style={{ height: '8rem', width: '100%' }}
    />
  );
}

function Label({ splittedTitle }) {
  return (
    <div className="flex flex-col items-start justify-center">
      <h1 className="font-bold text-3xl" style={{ marginBottom: '-0.6rem' }}>{splittedTitle[0]}</h1>

      <h2 className="m-0 text-2xl tracking-wider">{splittedTitle[1]}</h2>
    </div>
  );
}

export default PieChart;
