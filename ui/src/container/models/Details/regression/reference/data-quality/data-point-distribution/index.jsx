import { modelsApiSlice } from '@State/models/api';
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
  NewHeader,
  Pin,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router-dom';
import { CHART_COLOR } from '@Helpers/common-chart-options';
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

      <DataPointDistributionCounter />

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

          <span>{`${fullNumber} data point`}</span>

        </div>
      )}
      modifier="basis-1/6 shadow"
      size="small"
      type="secondary"
    />
  );
}

function DataPointDistributionChart() {
  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const title = model?.target.name;

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const classMetrics = data?.dataQuality.targetMetrics.histogram;

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
          }}
          title={<SectionTitle size="small" title={title} />}
        />
      )}
      main={(
        <div>
          <ReactEchartsCore
            key={uuid}
            echarts={echarts}
            onChartReady={handleOnChartReady}
            option={chartOptions(classMetrics, CHART_COLOR.REFERENCE)}
            style={{ height: '20rem', width: '100%' }}
          />
        </div>
      )}
      modifier="w-full shadow overflow-auto max-w-full "
      size="small"
    />
  );
}

export default DataPointDistribution;
