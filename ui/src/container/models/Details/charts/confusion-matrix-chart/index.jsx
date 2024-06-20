import ReactEchartsCore from 'echarts-for-react/lib/core';
import { HeatmapChart } from 'echarts/charts';
import {
  GridComponent,
  VisualMapComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { Board, SectionTitle } from '@radicalbit/radicalbit-design-system';
import confusionMatrixOptions from './options';

echarts.use([
  GridComponent,
  HeatmapChart,
  VisualMapComponent,
]);

function ConfusionMatrix({ dataset, labelClass, colors }) {
  if (!dataset) return false;

  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  return (
    <Board
      header={<SectionTitle size="small" title="Confusion Matrix" />}
      main={(
        <ReactEchartsCore
          echarts={echarts}
          onChartReady={handleOnChartReady}
          option={confusionMatrixOptions(dataset, labelClass, colors)}
          style={{ height: '100%' }}
        />
      )}
      modifier="min-h-[25rem] h-[25rem]"
      size="small"
    />
  );
}

export default ConfusionMatrix;
