import JobStatus from '@Components/JobStatus';
import ConfusionMatrix from '@Components/charts/confusion-matrix-chart';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { useGetReferenceModelQualityQueryWithPolling } from '@State/models/polling-hook';
import {
  Board, DataTable, SectionTitle, Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import columns from './columns';

function BinaryClassificationModelQualityMetrics() {
  const { data, isLoading } = useGetReferenceModelQualityQueryWithPolling();

  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    const leftTableData = data ? [
      { label: MODEL_QUALITY_FIELD.ACCURACY, value: data.modelQuality.accuracy },
      { label: MODEL_QUALITY_FIELD.PRECISION, value: data.modelQuality.precision },
      { label: MODEL_QUALITY_FIELD.RECALL, value: data.modelQuality.recall },
      { label: MODEL_QUALITY_FIELD.F1, value: data.modelQuality.f1 },
    ] : [];

    const centerTableData = data ? [
      { label: 'False positive rate', value: data.modelQuality.falsePositiveRate },
      { label: 'True positive rate', value: data.modelQuality.truePositiveRate },
    ] : [];

    const rightTableData = data ? [
      { label: MODEL_QUALITY_FIELD.AREA_UNDER_ROC, value: data.modelQuality.areaUnderRoc },
      { label: MODEL_QUALITY_FIELD.AREA_UNDER_PR, value: data.modelQuality.areaUnderPr },
    ] : [];

    const confusionMatrixLabel = {
      xAxisLabel: ['1', '0'],
      yAxisLabel: ['0', '1'],
    };

    const confusionMatrixData = [
      [data.modelQuality.truePositiveCount, data.modelQuality.falsePositiveCount],
      [data.modelQuality.falseNegativeCount, data.modelQuality.trueNegativeCount],
    ];

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

          <ConfusionMatrix
            colors={[CHART_COLOR.WHITE, CHART_COLOR.REFERENCE]}
            dataset={confusionMatrixData}
            labelClass={confusionMatrixLabel}
          />
        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(BinaryClassificationModelQualityMetrics);
