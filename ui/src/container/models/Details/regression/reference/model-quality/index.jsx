import JobStatus from '@Components/JobStatus';
import PredictedActualChart from '@Components/charts/predicted-actual-chart';
import ResidualBucketChart from '@Components/charts/residual-bucket-chart';
import ResidualScatterPlot from '@Components/charts/residual-scatter-plot';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import { JOB_STATUS, numberFormatter } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetReferenceModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { faChartArea, faChartLine } from '@fortawesome/free-solid-svg-icons';
import {
  Board,
  DataTable,
  FontAwesomeIcon,
  SectionTitle,
  Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import columns from './columns';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function RegressionModelQualityMetrics() {
  const { data, isLoading, isSuccess } = useGetReferenceModelQualityQueryWithPolling();

  const jobStatus = data?.jobStatus;

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (!isSuccess) {
    return false;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (<RegressionModelQualityMetricsInner />);
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function RegressionModelQualityMetricsInner() {
  const mode = useGetModeParam();

  if (mode === MODE.TABLE) {
    return (
      <div className="flex flex-col gap-4 py-4 px-4 h-full">
        <div>
          <PerformanceBoard />
        </div>

        <div className="flex flex-row gap-4">

          <div className="basis-1/6">
            <CorrelationCoefficientCounter />
          </div>

          <div className="basis-5/6">
            <ResidualScatterPlotBoard />
          </div>

          <FaCode />
        </div>

      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 py-4 px-4 h-full">
      <div>
        <PerformanceBoard />
      </div>

      <div className="flex flex-row gap-4">

        <div className="flex flex-col gap-4 ">
          <KsPValueCounter />

          <KsStatisticsCounter />
        </div>

        <div className="basis-5/6">

          <PredictedActualBoardChart />

        </div>

        <FaCode />
      </div>

      <BucketChart />

    </div>

  );
}

function PerformanceBoard() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();

  const leftTableData = data ? [
    { label: MODEL_QUALITY_FIELD.MSE, value: data.modelQuality.mse },
    { label: MODEL_QUALITY_FIELD.RMSE, value: data.modelQuality.rmse },
  ] : [];

  const centerTableData = data ? [
    { label: MODEL_QUALITY_FIELD.MAE, value: data.modelQuality.mae },
    { label: MODEL_QUALITY_FIELD.MAPE, value: data.modelQuality.mape },
  ] : [];

  const rightTableData = data ? [
    { label: MODEL_QUALITY_FIELD.R2, value: data.modelQuality.r2 },
    { label: MODEL_QUALITY_FIELD.ADJ_R2, value: data.modelQuality.adjR2 },
    { label: MODEL_QUALITY_FIELD.VARIANCE, value: data.modelQuality.variance },
  ] : [];

  return (
    <Board
      header={<SectionTitle size="small" title="Performance metrics" />}
      main={(
        <div className="flex flew-row gap-4">
          <DataTable
            columns={columns}
            dataSource={leftTableData}
            modifier="basis-1/3"
            pagination={false}
            rowKey={({ label }) => label}
            size="small"
          />

          <DataTable
            columns={columns}
            dataSource={centerTableData}
            modifier="basis-1/3"
            pagination={false}
            rowKey={({ label }) => label}
            size="small"
          />

          <DataTable
            columns={columns}
            dataSource={rightTableData}
            modifier="basis-1/3"
            pagination={false}
            rowKey={({ label }) => label}
            size="small"
          />
        </div>
        )}
      size="small"
      type="secondary"
    />
  );
}

function BucketChart() {
  const { data, isLoading, isSuccess } = useGetReferenceModelQualityQueryWithPolling();

  const dataset = data?.modelQuality.residuals.histogram;

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (!isSuccess) {
    return false;
  }

  return (
    <Board
      header={(<SectionTitle size="small" title="Residuals" />)}
      main={(<ResidualBucketChart color={CHART_COLOR.REFERENCE} dataset={dataset} />)}
      size="small"
    />
  );
}

function ResidualScatterPlotBoard() {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });

  const predictionName = model?.outputs.prediction?.name;

  const { data } = useGetReferenceModelQualityQueryWithPolling();

  const predictions = data?.modelQuality.residuals.predictions ?? [];
  const standardizedResiduals = data?.modelQuality.residuals.standardizedResiduals ?? [];

  const dataset = predictions.map((p, idx) => ([p, standardizedResiduals[idx]]));
  const xAxisLabel = `${predictionName}`;
  const yAxisLabel = 'standardized residuals';

  return (
    <Board
      header={(<SectionTitle size="small" title="Residuals plot" />)}
      main={(
        <ResidualScatterPlot
          color={CHART_COLOR.REFERENCE}
          dataset={dataset}
          xAxisLabel={xAxisLabel}
          yAxisLabel={yAxisLabel}
        />
    )}
      size="small"
    />
  );
}

function PredictedActualBoardChart() {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });

  const predictionName = model?.outputs.prediction?.name;
  const targetName = model?.target?.name;

  const xAxisLabel = `${targetName}`;
  const yAxisLabel = `${predictionName}`;

  const title = `${yAxisLabel} vs ${xAxisLabel}`;

  const { data } = useGetReferenceModelQualityQueryWithPolling();

  const predictions = data?.modelQuality.residuals.predictions ?? [];
  const targets = data?.modelQuality.residuals.targets ?? [];
  const regressionLine = data?.modelQuality.residuals.regressionLine;

  const dataset = {
    data: predictions.map((p, idx) => ([targets[idx], p])),
    regressionLine,
  };

  return (
    <Board
      header={(<SectionTitle size="small" title={title} />)}
      main={(
        <PredictedActualChart
          color={CHART_COLOR.REFERENCE}
          dataset={dataset}
          xAxisLabel={xAxisLabel}
          yAxisLabel={yAxisLabel}
        />
    )}
      size="small"
    />
  );
}

function CorrelationCoefficientCounter() {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });

  const predictionName = model?.outputs.prediction?.name;
  const targetName = model?.target?.name;

  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const correlationCoefficient = data?.modelQuality.residuals.correlationCoefficient;
  const formattedNumber = correlationCoefficient ? numberFormatter().format(correlationCoefficient) : '--';

  const title = `Correlation ${predictionName}/${targetName}`;

  return (
    <Board
      header={<SectionTitle size="small" title={title} />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{formattedNumber}</div>
          </div>
        </div>
      )}
      modifier="h-[12rem] shadow"
      size="small"
      type="secondary"
    />
  );
}

function KsPValueCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const ksPvalue = data?.modelQuality.residuals.ks.pValue;

  const formattedNumber = ksPvalue ? Number.parseFloat(ksPvalue).toExponential(2) : '--';

  return (
    <Board
      header={<SectionTitle size="small" title="KS test of normality for residuals : pValue" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{formattedNumber}</div>
          </div>
        </div>
      )}
      modifier="h-[12rem] shadow"
      size="small"
      type="secondary"
    />
  );
}

function KsStatisticsCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const ksStatistics = data?.modelQuality.residuals.ks.statistic;
  const formattedNumber = ksStatistics ? numberFormatter().format(ksStatistics) : '--';

  return (
    <Board
      header={<SectionTitle size="small" title="KS statistics test of normality for residuals" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{formattedNumber}</div>
          </div>
        </div>
      )}
      modifier="h-[12rem] shadow"
      size="small"
      type="secondary"
    />
  );
}

function FaCode() {
  const [searchParams, setSearchParams] = useSearchParams();
  const mode = useGetModeParam();

  const handleOnClickCode = () => {
    searchParams.set('mode', MODE.CHART);
    setSearchParams(searchParams);
  };

  const handleOnClickTable = () => {
    searchParams.set('mode', MODE.TABLE);
    setSearchParams(searchParams);
  };

  if (mode === MODE.CHART) {
    return <FontAwesomeIcon icon={faChartArea} onClick={handleOnClickTable} size="xl" />;
  }

  return <FontAwesomeIcon icon={faChartLine} onClick={handleOnClickCode} size="xl" />;
}

const useGetModeParam = () => {
  const [searchParams] = useSearchParams();

  const mode = searchParams.get('mode');

  return mode === MODE.CHART ? MODE.CHART : MODE.TABLE;
};

const MODE = {
  CHART: 'table',
  TABLE: 'chart',
};

export default memo(RegressionModelQualityMetrics);
