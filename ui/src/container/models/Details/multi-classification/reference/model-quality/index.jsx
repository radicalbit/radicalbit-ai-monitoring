import JobStatus from '@Components/JobStatus';
import ConfusionMatrix from '@Components/charts/confusion-matrix-chart';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import { JOB_STATUS, numberFormatter } from '@Src/constants';
import { useGetReferenceModelQualityQueryWithPolling } from '@State/models/polling-hook';
import {
  Board,
  SectionTitle,
  Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import ClassTableMetrics from './class-table-metrics';

function MultiClassificationModelQualityMetrics() {
  const { data, isLoading } = useGetReferenceModelQualityQueryWithPolling();

  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <Spinner spinning={isLoading}>
        <div className="flex flex-col gap-4 py-4">

          <GlobalMetrics />

          <ClassTableMetrics />

        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function GlobalMetrics() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const labels = data?.modelQuality.classes ?? [];
  const confusionMatrixData = data?.modelQuality.globalMetrics.confusionMatrix ?? [];

  const confusionMatrixLabel = {
    xAxisLabel: labels,
    yAxisLabel: labels.toReversed(),
  };

  return (
    <div className="flex flex-row gap-4">
      <div className="flex flex-col gap-4 basis-1/6">
        <AccuracyCounter />

        <F1ScoreCounter />

        <ClassCounter />
      </div>

      <div className="w-full">
        <ConfusionMatrix
          colors={[CHART_COLOR.WHITE, CHART_COLOR.REFERENCE]}
          dataset={confusionMatrixData}
          height="36rem"
          labelClass={confusionMatrixLabel}
        />
      </div>
    </div>
  );
}

function AccuracyCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const accuracy = data?.modelQuality.globalMetrics.accuracy ?? 0;
  const accuracyFormatted = numberFormatter().format(accuracy);

  return (
    <Board
      header={<SectionTitle size="small" title="Accuracy" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            {accuracyFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

function F1ScoreCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const f1Score = data?.modelQuality.globalMetrics.f1 ?? 0;
  const f1ScoreFormatted = numberFormatter().format(f1Score);

  return (
    <Board
      header={<SectionTitle size="small" title="F1 Score" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            {f1ScoreFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

function ClassCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const classes = data?.modelQuality.classes ?? [];

  return (
    <Board
      header={<SectionTitle size="small" title="Classes" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            {classes.length}
          </div>

        </div>
      )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

export default memo(MultiClassificationModelQualityMetrics);
