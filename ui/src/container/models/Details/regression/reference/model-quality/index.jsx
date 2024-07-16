import JobStatus from '@Components/JobStatus';
import PredictedActualChart from '@Components/charts/predicted-actual-chart';
import ResidualBucketChart from '@Components/charts/residual-bucket-chart';
import ResidualScatterPlot from '@Components/charts/residual-scatter-plot';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import { JOB_STATUS } from '@Src/constants';
import { modelsApiSlice } from '@Src/store/state/models/api';
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
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import columns from './columns';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function RegressionModelQualityMetrics() {
  const { data, isLoading } = useGetReferenceModelQualityQueryWithPolling();

  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <Spinner spinning={isLoading}>
        <div className="flex flex-col gap-4 py-4">
          <PerformanceBoard />

          <ScatterPlot />

          <BucketChart />

        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
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

function ScatterPlot() {
  const mode = useGetModeParam();

  const { isLoading, isSuccess } = useGetReferenceModelQualityQueryWithPolling();

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (!isSuccess) {
    return false;
  }

  if (mode === MODE.TABLE) {
    return (<ResidualScatterPlotBoard />);
  }

  return (<PredictedActualBoardChart />);
}

function ResidualScatterPlotBoard() {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });

  const predictionName = model?.outputs.prediction?.name;

  const { data } = useGetReferenceModelQualityQueryWithPolling();

  const predictions = data?.modelQuality.residuals.predictions ?? [];
  const standardizedResiduals = data?.modelQuality.residuals.standardizedResiduals ?? [];

  const dataset = predictions.map((p, idx) => ([p, standardizedResiduals[idx]]));
  const xAxisLabel = `predicted ${predictionName}`;
  const yAxisLabel = 'standardized residuals';
  return (
    <Board
      header={(
        <div className="flex flex-row items-center space-between">
          <SectionTitle size="small" title="Residual plot" />

          <div className="flex">
            <FaCode />
          </div>

        </div>
  )}
      main={(<ResidualScatterPlot color={CHART_COLOR.REFERENCE} dataset={dataset} xAxisLabel={xAxisLabel} yAxisLabel={yAxisLabel} />)}
      size="small"
    />
  );
}

function PredictedActualBoardChart() {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });

  const predictionName = model?.outputs.prediction?.name;
  const targetName = model?.target?.name;

  const xAxisLabel = `predicted values for ${predictionName}`;
  const yAxisLabel = `Actual values for ${targetName}`;

  const { data } = useGetReferenceModelQualityQueryWithPolling();

  const predictions = data?.modelQuality.residuals.predictions ?? [];
  const targets = data?.modelQuality.residuals.targets ?? [];

  const dataset = predictions.map((p, idx) => ([p, targets[idx]]));

  return (
    <Board
      header={(
        <div className="flex flex-row items-center space-between">
          <SectionTitle size="small" title="Predicted vs Actual" />

          <div className="flex">
            <FaCode />
          </div>

        </div>
    )}
      main={(<PredictedActualChart color={CHART_COLOR.REFERENCE} dataset={dataset} xAxisLabel={xAxisLabel} yAxisLabel={yAxisLabel} />)}
      size="small"
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
