import { modelsApiSlice } from '@State/models/api';
import { useGetCurrentDataQualityQueryWithPolling } from '@State/models/polling-hook';
import {
  Board,
  NewHeader,
  Pin,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import ReactEchartsCore from 'echarts-for-react/lib/core';
import { BarChart } from 'echarts/charts';
import {
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { useParams } from 'react-router-dom';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import chartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  LegendComponent,
  BarChart,
  DataZoomComponent,
  DataZoomInsideComponent,
  DataZoomSliderComponent,
]);

const { useGetModelByUUIDQuery, useGetReferenceDataQualityQuery } = modelsApiSlice;

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
      <div className="flex flex-col gap-4 basis-1/6 ">
        <DataPointDistributionCounter />

        <ClassCounter />
      </div>

      <DataPointDistributionChart />

    </div>
  );
}

function DataPointDistributionCounter() {
  const { data } = useGetCurrentDataQualityQueryWithPolling();
  const nObservations = data?.dataQuality.nObservations ?? 0;

  const { figures, letter } = numberCompactFormatter(nObservations);
  const fullNumber = numberFormatter(nObservations);

  return (
    <Board
      header={<SectionTitle size="small" title="Current" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{figures}</div>

            <div className="text-3xl">{letter}</div>
          </div>

          <span>
            {`${fullNumber} data point`}
          </span>

        </div>
      )}
      modifier="shadow"
      size="small"
      type="primary"
    />
  );
}

function ClassCounter() {
  const { uuid } = useParams();

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const nObservations = data?.dataQuality.classMetrics.length ?? 0;

  return (
    <Board
      header={<SectionTitle size="small" title="Classes" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{nObservations}</div>
          </div>

        </div>
      )}
      modifier="shadow"
      size="small"
      type="secondary"
    />
  );
}

function DataPointDistributionChart() {
  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const title = model?.target.name;

  const { data: currentData } = useGetCurrentDataQualityQueryWithPolling();

  const currentClassMetrics = currentData?.dataQuality.classMetrics ?? [];
  const sortedCurrentClassMetrics = [...currentClassMetrics].sort((a, b) => a.name - b.name);

  const { data: referenceData } = useGetReferenceDataQualityQuery({ uuid });
  const referenceClassMetrics = referenceData?.dataQuality.classMetrics ?? [];
  const sortedReferenceClassMetrics = [...referenceClassMetrics].sort((a, b) => a.name - b.name);

  const handleOnChartReady = (echart) => {
    // To handle the second opening of a modal when the rtkq hook read from cache
    // and the echart graph will render immediately.
    setTimeout(echart.resize);
  };

  return (
    <Board
      header={(
        <NewHeader
          details={{
            one: <Pin color={CHART_COLOR.REFERENCE_LIGHT} label="Reference" size="small" />,
            two: <Pin color={CHART_COLOR.CURRENT_LIGHT} label="Current" size="small" />,
          }}
          title={<SectionTitle size="small" title={title} />}
        />
)}
      main={(
        <ReactEchartsCore
          echarts={echarts}
          onChartReady={handleOnChartReady}
          option={chartOptions(title, sortedReferenceClassMetrics, sortedCurrentClassMetrics)}
          style={{ height: '20rem', width: '100%' }}
        />
      )}
      modifier="w-full shadow overflow-auto max-w-full "
      size="small"
    />
  );
}

export default DataPointDistribution;
