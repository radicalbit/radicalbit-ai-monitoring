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
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
} from 'echarts/components';
import * as echarts from 'echarts/lib/echarts';
import { useParams } from 'react-router';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import chartOptions from './options';

echarts.use([
  GridComponent,
  MarkPointComponent,
  MarkLineComponent,
  LegendComponent,
  BarChart,
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
      <div className="basis-1/6">
        <DataPointDistributionCounter />
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
      modifier="h-full shadow"
      size="small"
      type="primary"
    />
  );
}

function DataPointDistributionChart() {
  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const title = model?.target.name;

  const { data: currentData } = useGetCurrentDataQualityQueryWithPolling();

  const currentClassMetrics = currentData?.dataQuality.classMetrics ?? [];

  const { data: referenceData } = useGetReferenceDataQualityQuery({ uuid });
  const referenceClassMetrics = referenceData?.dataQuality.classMetrics ?? [];

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
            one: (
              <div className="flex flex-row gap-2 items-center">
                <div className="flex flex-row gap-1 items-center">
                  <Pin color={CHART_COLOR.REFERENCE_LIGHT} size="small" />

                  <label>Reference</label>
                </div>

                <div className="flex flex-row gap-1 items-center">
                  <Pin color={CHART_COLOR.CURRENT_LIGHT} size="small" />

                  <label>Current</label>
                </div>
              </div>

            ),
          }}
          title={<SectionTitle size="small" title={title} />}
        />
)}
      main={(
        <div>
          <ReactEchartsCore
            echarts={echarts}
            onChartReady={handleOnChartReady}
            option={chartOptions(title, referenceClassMetrics, currentClassMetrics)}
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
