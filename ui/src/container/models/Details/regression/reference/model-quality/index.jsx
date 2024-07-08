import JobStatus from '@Components/JobStatus';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { useGetReferenceModelQualityQueryWithPolling } from '@State/models/polling-hook';
import {
  Board,
  DataTable,
  SectionTitle,
  Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import columns from './columns';

function MultiClassificationModelQualityMetrics() {
  const { data, isLoading } = useGetReferenceModelQualityQueryWithPolling();

  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    if (jobStatus === JOB_STATUS.SUCCEEDED) {
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
      ] : [];

      return (
        <Spinner spinning={isLoading}>
          <div className="flex flex-col gap-4 py-4">
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

          </div>
        </Spinner>
      );
    }
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(MultiClassificationModelQualityMetrics);
