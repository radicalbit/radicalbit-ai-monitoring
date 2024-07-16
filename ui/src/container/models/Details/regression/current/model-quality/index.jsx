import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import PredictedActualChart from '@Components/charts/predicted-actual-chart';
import ResidualBucketChart from '@Components/charts/residual-bucket-chart';
import ResidualScatterPlot from '@Components/charts/residual-scatter-plot';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import { JOB_STATUS, numberFormatter } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetCurrentModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { faChartArea, faChartLine } from '@fortawesome/free-solid-svg-icons';
import {
  Board, DataTable, FontAwesomeIcon, SectionTitle, Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import {
  AdjR2Chart,
  MaeChart,
  MapeChart,
  MseChart,
  R2Chart,
  RmseChart,
  VarianceChart,
} from './charts';
import columns from './columns';

const { useGetReferenceModelQualityQuery, useGetModelByUUIDQuery } = modelsApiSlice;

function RegressionModelQualityMetrics() {
  const { data, isLoading, isError } = useGetCurrentModelQualityQueryWithPolling();

  const jobStatus = data?.jobStatus;

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (isError) {
    return <SomethingWentWrong />;
  }

  if (!data) {
    return <JobStatus jobStatus={JOB_STATUS.MISSING_CURRENT} />;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (<RegressionModelQualityMetricsInner />
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function RegressionModelQualityMetricsInner() {
  const mode = useGetModeParam();

  if (mode === MODE.TABLE) {
    return (
      <div className="flex flex-col gap-4 py-4 ">
        <div>
          <PerformanceBoard />
        </div>

        <div className="flex flex-row gap-4">

          <div className="basis-1/5">
            <CorrelationCoefficientCounter />
          </div>

          <div className="basis-4/5">
            <ResidualScatterPlotBoard />
          </div>

          <FaCode />
        </div>

        <div className="flex flex-col gap-4">
          <MseChart />

          <RmseChart />

          <MaeChart />

          <MapeChart />

          <R2Chart />

          <AdjR2Chart />

          <VarianceChart />
        </div>

      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 py-4 ">
      <PerformanceBoard />

      <div className="flex flex-row gap-4 h-full">
        <div className="flex flex-col gap-4 basis-1/5">
          <KsPValueCounter />

          <KsStatisticsCounter />
        </div>

        <div className="flex gap-4 basis-4/5">
          <div className="flex flex-col gap-4 w-full">

            <PredictedActualBoardChart />

            <BucketChart />

          </div>

        </div>

        <FaCode />
      </div>

      <div className="flex flex-col gap-4">
        <MseChart />

        <RmseChart />

        <MaeChart />

        <MapeChart />

        <R2Chart />

        <AdjR2Chart />

        <VarianceChart />
      </div>

    </div>

  );
}

function PerformanceBoard() {
  const { uuid } = useParams();

  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceMse = referenceData?.modelQuality?.mse;
  const referenceRmse = referenceData?.modelQuality?.rmse;
  const referenceMae = referenceData?.modelQuality?.mae;
  const referenceMape = referenceData?.modelQuality?.mape;
  const referenceR2 = referenceData?.modelQuality?.r2;
  const referenceAdjR2 = referenceData?.modelQuality?.adjR2;
  const referenceVariance = referenceData?.modelQuality?.variance;

  const leftTableData = currentData ? [
    {
      label: MODEL_QUALITY_FIELD.MSE,
      referenceValue: referenceMse,
      currentValue: currentData.modelQuality.globalMetrics.mse,
    },
    {
      label: MODEL_QUALITY_FIELD.RMSE,
      referenceValue: referenceRmse,
      currentValue: currentData.modelQuality.globalMetrics.rmse,
    },
  ] : [];

  const centerTableData = currentData ? [
    {
      label: MODEL_QUALITY_FIELD.MAE,
      referenceValue: referenceMae,
      currentValue: currentData.modelQuality.globalMetrics.mae,
    },
    {
      label: MODEL_QUALITY_FIELD.MAPE,
      referenceValue: referenceMape,
      currentValue: currentData.modelQuality.globalMetrics.mape,
    },
  ] : [];

  const rightTableData = currentData ? [
    {
      label: MODEL_QUALITY_FIELD.R2,
      referenceValue: referenceR2,
      currentValue: currentData.modelQuality.globalMetrics.r2,
    },
    {
      label: MODEL_QUALITY_FIELD.ADJ_R2,
      referenceValue: referenceAdjR2,
      currentValue: currentData.modelQuality.globalMetrics.adjR2,
    },
    {
      label: MODEL_QUALITY_FIELD.VARIANCE,
      referenceValue: referenceVariance,
      currentValue: currentData.modelQuality.globalMetrics.variance,
    },
  ] : [];

  return (
    <Board
      header={<SectionTitle size="small" title="Performance metrics" />}
      main={(
        <div className="flex flew-row gap-16">
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
      modifier="shadow"
      size="small"
      type="primary-light"
    />
  );
}

function BucketChart() {
  const { data, isLoading, isSuccess } = useGetCurrentModelQualityQueryWithPolling();

  const dataset = data?.modelQuality.globalMetrics.residuals.histogram;

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (!isSuccess) {
    return false;
  }

  return (
    <Board
      header={(<SectionTitle size="small" title="Residuals" />)}
      main={(<ResidualBucketChart color={CHART_COLOR.CURRENT} dataset={dataset} />)}
      size="small"
    />
  );
}

function ResidualScatterPlotBoard() {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });

  const predictionName = model?.outputs.prediction?.name;

  const { data } = useGetCurrentModelQualityQueryWithPolling();

  const predictions = data?.modelQuality.globalMetrics.residuals.predictions ?? [];
  const standardizedResiduals = data?.modelQuality.globalMetrics.residuals.standardizedResiduals ?? [];

  const dataset = predictions.map((p, idx) => ([p, standardizedResiduals[idx]]));
  const xAxisLabel = `${predictionName}`;
  const yAxisLabel = 'standardized residuals';
  return (
    <Board
      header={(<SectionTitle size="small" title="Residuals plot" />)}
      main={(
        <ResidualScatterPlot
          color={CHART_COLOR.CURRENT}
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

  const { data } = useGetCurrentModelQualityQueryWithPolling();

  const predictions = data?.modelQuality.globalMetrics.residuals.predictions ?? [];
  const targets = data?.modelQuality.globalMetrics.residuals.targets ?? [];

  const dataset = predictions.map((p, idx) => ([targets[idx], p]));

  return (
    <Board
      header={(<SectionTitle size="small" title={title} />)}
      main={(
        <PredictedActualChart
          color={CHART_COLOR.CURRENT}
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

  const { data } = useGetCurrentModelQualityQueryWithPolling();
  const correlationCoefficient = data?.modelQuality.globalMetrics.residuals.correlationCoefficient;
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
  const { data } = useGetCurrentModelQualityQueryWithPolling();
  const ksPvalue = data?.modelQuality.globalMetrics.residuals.ks.pValue;

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
  const { data } = useGetCurrentModelQualityQueryWithPolling();
  const ksStatistics = data?.modelQuality.globalMetrics.residuals.ks.statistic;
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
    return <FontAwesomeIcon icon={faChartArea} onClick={handleOnClickTable} size="lg" />;
  }

  return <FontAwesomeIcon icon={faChartLine} onClick={handleOnClickCode} size="lg" />;
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
