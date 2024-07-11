import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetCurrentModelQualityQueryWithPolling } from '@State/models/polling-hook';
import {
  Board, DataTable, SectionTitle, Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { useParams } from 'react-router';
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

const { useGetReferenceModelQualityQuery } = modelsApiSlice;

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
    return (
      <Spinner spinning={isLoading}>
        <div className="flex flex-col gap-4 py-4">
          <PerformanceBoard />

          <MseChart />

          <RmseChart />

          <MaeChart />

          <MapeChart />

          <R2Chart />

          <AdjR2Chart />

          <VarianceChart />
        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
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
  const referenceAdjR2 = referenceData?.modelQuality?.ajdR2;
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
      currentValue: currentData.modelQuality.globalMetrics.ajdR2,
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

export default memo(RegressionModelQualityMetrics);
