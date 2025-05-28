import ReactEchartsCore from 'echarts-for-react/lib/core';
import { HeatmapChart } from 'echarts/charts';
import {
  GridComponent,
  VisualMapComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { Board, SectionTitle, Void } from '@radicalbit/radicalbit-design-system';
import LogoSquared from '@Img/logo-collapsed.svg';
import confusionMatrixOptions from './options';

echarts.use([
  GridComponent,
  HeatmapChart,
  VisualMapComponent,
]);

function ConfusionMatrix({
  dataset, labelClass, colors, height = '20rem',
}) {
  if (!dataset) {
    return false;
  }

  if (dataset.length > 10) {
    return (
      <Void
        description={(
          <>
            That chart can be shown only for a dataset
            <br />
            that contains less then 10 classes
          </>
        )}
        image={<LogoSquared />}
        title="Confusion Matrix"
      />
    );
  }

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
          style={{ height }}
        />
      )}
      size="small"
    />
  );
}

export default ConfusionMatrix;
