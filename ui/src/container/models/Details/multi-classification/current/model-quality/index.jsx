import JobStatus from '@Components/JobStatus';
import ConfusionMatrix from '@Components/charts/confusion-matrix-chart';
import { CHART_COLOR } from '@Helpers/common-chart-options';
import { JOB_STATUS, numberFormatter } from '@Src/constants';
import { useGetCurrentModelQualityQueryWithPolling, useGetReferenceModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { faChartLine, faCode } from '@fortawesome/free-solid-svg-icons';
import { FormbitContextProvider } from '@radicalbit/formbit';
import {
  Board,
  Button,
  FontAwesomeIcon,
  SectionTitle,
  Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo, useState } from 'react';
import MulticlassChartMetrics from './class-chart-metrics';
import ClassTableMetrics from './class-table-metrics';
import SearchChart from './search-chart';

const initialValues = { __metadata: { selectedCharts: [] } };

function MultiClassificationModelQualityMetrics() {
  const { data, isLoading } = useGetCurrentModelQualityQueryWithPolling();
  console.debug('🚀 ~ MultiClassificationModelQualityMetrics ~ data:', data);
  const { isLoading: referenceIsLoading } = useGetReferenceModelQualityQueryWithPolling();

  const [showChart, setShowChart] = useState(false);

  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    if (showChart) {
      return (
        <Spinner spinning={isLoading}>
          <div className="flex flex-col gap-4 py-4">

            <Button onClick={() => setShowChart(false)}>
              <FontAwesomeIcon icon={faCode} />
            </Button>

            <FormbitContextProvider initialValues={initialValues}>

              <SearchChart />

              <MulticlassChartMetrics />

            </FormbitContextProvider>

          </div>
        </Spinner>
      );
    }

    return (
      <Spinner spinning={isLoading || referenceIsLoading}>
        <div className="flex flex-col gap-4 py-4">

          <Button onClick={() => setShowChart(true)}>
            <FontAwesomeIcon icon={faChartLine} />
          </Button>

          <GlobalMetrics />

          <ClassTableMetrics />

        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function GlobalMetrics() {
  const { data } = useGetCurrentModelQualityQueryWithPolling();
  const labels = data?.modelQuality.classes ?? [];
  const confusionMatrixData = data?.modelQuality.globalMetrics.confusionMatrix ?? [];

  const confusionMatrixLabel = {
    xAxisLabel: labels,
    yAxisLabel: labels.toReversed(),
  };

  const confusionMatrixHeight = (labels.length > 13) ? labels.length * 1.8 : '22';

  return (
    <div className="flex flex-row gap-4">
      <div className="flex flex-col gap-4 basis-1/6">
        <AccuracyCounter />

        <F1ScoreCounter />

        <ClassCounter />
      </div>

      <div className="w-full">
        <ConfusionMatrix
          colors={[CHART_COLOR.WHITE, CHART_COLOR.CURRENT]}
          dataset={confusionMatrixData}
          height={`${confusionMatrixHeight}rem`}
          labelClass={confusionMatrixLabel}
        />
      </div>
    </div>
  );
}

function AccuracyCounter() {
  const { data } = useGetCurrentModelQualityQueryWithPolling();
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
      type="primary"
    />
  );
}

function F1ScoreCounter() {
  const { data } = useGetCurrentModelQualityQueryWithPolling();
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
      type="primary"
    />
  );
}

function ClassCounter() {
  const { data } = useGetCurrentModelQualityQueryWithPolling();
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
