import ReactEchartsCore from 'echarts-for-react/lib/core';
import { LineChart as LineChartEchart } from 'echarts/charts';
import {
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  TooltipComponent,
  TitleComponent,
  LegendScrollComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import {
  Board,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import lineChartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  LegendComponent,
  LegendScrollComponent,
  LineChartEchart,
  TooltipComponent,
  TitleComponent,
]);

function LineChart({
  title, currentData, referenceData = [],
}) {
  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  if (!currentData) {
    return false;
  }

  return (
    <Board
      header={(<SectionTitle size="small" title={title} />)}
      main={(
        <ReactEchartsCore
          echarts={echarts}
          notMerge
          onChartReady={handleOnChartReady}
          option={lineChartOptions(currentData, referenceData)}
          style={{ height: '24rem' }}
        />
      )}
      size="small"
    />
  );
}

export default LineChart;
