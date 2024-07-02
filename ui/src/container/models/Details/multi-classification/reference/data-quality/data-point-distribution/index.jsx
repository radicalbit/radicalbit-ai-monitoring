import { modelsApiSlice } from '@Src/store/state/models/api';
import ReactEchartsCore from 'echarts-for-react/lib/core';
import { BarChart } from 'echarts/charts';
import {
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import {
  Board,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';
import chartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  LegendComponent,
  BarChart,
]);

const { useGetReferenceDataQualityQuery, useGetModelByUUIDQuery } = modelsApiSlice;

const numberFormatter = (value) => new Intl.NumberFormat('it-IT').format(value);

const numberCompactFormatter = (value, maximumSignificantDigits) => {
  const str = Intl.NumberFormat('en-EN', { notation: 'compact', maximumSignificantDigits }).format(value);

  const re = /(\d*\.?\d+)([a-zA-Z]*)/;
  const [, figures, letter] = re.exec(str);

  return { figures, letter };
};

function DataPointDistribution() {
  return (
    <div className="flex flex-row gap-4">
      <div className="basis-1/5">
        <DataPointDistributionCounter />
      </div>

      <DataPointDistributionChart />

    </div>
  );
}

function DataPointDistributionCounter() {
  const { uuid } = useParams();

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const nObservations = data?.dataQuality.nObservations ?? 0;

  const { figures, letter } = numberCompactFormatter(nObservations);
  const fullNumber = numberFormatter(nObservations);

  return (
    <Board
      header={<SectionTitle size="small" title="Reference" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{figures}</div>

            <div className="text-3xl">{letter}</div>
          </div>

          <label>
            <p>{`${fullNumber} data point`}</p>
          </label>

        </div>
      )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

function DataPointDistributionChart() {
  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const title = model?.target.name;
  const modelType = model?.modelType;

  const { data } = useGetReferenceDataQualityQuery({ uuid });

  const classMetrics = data?.dataQuality.classMetrics ?? {};

  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  return (
    <Board
      header={<SectionTitle size="small" title={title} />}
      main={(
        <div>
          <ReactEchartsCore
            echarts={echarts}
            onChartReady={handleOnChartReady}
            option={chartOptions(title, classMetrics, modelType)}
            style={{ height: '100%' }}

          />
        </div>
      )}
      modifier="w-full h-full shadow"
      size="small"
    />
  );
}

export default DataPointDistribution;
