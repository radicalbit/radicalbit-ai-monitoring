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

          {/* <ClassTableMetrics /> */}

        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function GlobalMetrics() {
  return (
    <div className="flex flex-row gap-4 h-full w-full">

      <div className="flex flex-col gap-4 h-full">

        <R2Counter />

        <AdjR2Counter />

      </div>

      <MseCounter />

      <RmseCounter />

      <MaeCounter />

      <MapeCounter />

      <KolmogorovSmirnovCounter />

    </div>

  );
}

function R2Counter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const r2 = data?.modelQuality.r2;
  const r2Formatted = numberFormatter().format(r2);

  return (
    <Board
      header={<SectionTitle size="small" title="R-squared" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            { r2 === null ? '--' : r2Formatted}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"
      type="secondary"
    />
  );
}

function MaeCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const mae = data?.modelQuality.mae;
  const maeFormatted = numberFormatter().format(mae);

  return (
    <Board
      header={<SectionTitle size="small" title="Mae" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            {mae === null ? '--' : maeFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"

    />
  );
}

function MseCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const mse = data?.modelQuality.mse ?? 0;
  const mseFormatted = numberFormatter().format(mse);

  return (
    <Board
      header={<SectionTitle size="small" title="Mse" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            { mse === null ? '--' : mseFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"
    />
  );
}
/* var name must be changed BEside
function VarCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const var = data?.modelQuality.get("var") ?? "--";
  const varFormatted = numberFormatter().format(var);

  return (
    <Board
      header={<SectionTitle size="small" title="F1 Score" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            {maeFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}
*/

function MapeCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const mape = data?.modelQuality.mape;
  const mapeFormatted = numberFormatter().format(mape);

  return (
    <Board
      header={<SectionTitle size="small" title="Mape" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            { mape === null ? '--' : `${mapeFormatted}%`}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"
    />
  );
}

function RmseCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const rmse = data?.modelQuality.rmse;
  const rmseFormatted = numberFormatter().format(rmse);

  return (
    <Board
      header={<SectionTitle size="small" title="Rmse" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            { rmse === null ? '--' : rmseFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"
    />
  );
}

function AdjR2Counter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const adjR2 = data?.modelQuality.adjR2;
  const adjR2Formatted = numberFormatter().format(adjR2);

  return (
    <Board
      header={<SectionTitle size="small" title="Adjusted R-squared" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            { adjR2 === null ? '--' : adjR2Formatted}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"
    />
  );
}

function KolmogorovSmirnovCounter() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const kol = data?.modelQuality.kol;
  const kolFormatted = numberFormatter().format(kol);

  return (
    <Board
      header={<SectionTitle size="small" title="Kolmogorov-Smirnov" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">

          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            { kol === null ? '--' : kolFormatted}
          </div>

        </div>
      )}
      modifier="h-full shadow basis-1/6"
      size="small"
      type="secondary"
    />
  );
}

export default memo(MultiClassificationModelQualityMetrics);
