import { DRIFT_TEST_ENUM } from '@Src/constants';
import { useGetCurrentDriftQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { Board, SectionTitle } from '@radicalbit/radicalbit-design-system';

function DataDriftHeader() {
  return (
    <div className="flex gap-4">
      <div className="basis-1/3">
        <TotalFeaturesCounter />
      </div>

      <div className="basis-1/3">
        <CategoricalFeaturesCounter />
      </div>

      <div className="basis-1/3">
        <NumericalFeaturesCounter />
      </div>
    </div>
  );
}

function TotalFeaturesCounter() {
  const { data } = useGetCurrentDriftQueryWithPolling();
  const featureMetrics = data?.drift.featureMetrics.filter((feature) => feature.driftCalc.hasDrift) ?? [];
  const featuresWithDriftCounter = featureMetrics.length;
  const featuresCounter = data?.drift.featureMetrics.length;

  if (featuresCounter === 0) {
    return (
      <Board
        header={<SectionTitle size="small" />}
        main={(
          <div className="flex flex-col h-full items-center justify-center gap-4">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>--</div>

            <div>Features with drift</div>
          </div>
          )}
        modifier="h-full shadow"
        size="small"
      />
    );
  }

  return (
    <Board
      header={<SectionTitle size="small" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          {/* FIXME: inline style */}
          <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
            {featuresWithDriftCounter}

            <small>
              /
              {featuresCounter}
            </small>
          </div>

          <div>Features with drift</div>
        </div>
        )}
      modifier="h-full shadow"
      size="small"
      type="primary"
    />

  );
}

function CategoricalFeaturesCounter() {
  const { data } = useGetCurrentDriftQueryWithPolling();

  const featureMetrics = data?.drift.featureMetrics ?? [];
  const categoricalWithDriftCounter = featureMetrics.filter((feature) => feature.driftCalc.type === DRIFT_TEST_ENUM.CHI2 && feature.driftCalc.hasDrift).length;
  const categoricalCounter = featureMetrics.filter((feature) => feature.driftCalc.type === DRIFT_TEST_ENUM.CHI2).length;

  if (categoricalCounter === 0) {
    return (
      <Board
        header={<SectionTitle size="small" />}
        main={(
          <div className="flex flex-col h-full items-center">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>--</div>

            <div>Categorical with drift</div>
          </div>
          )}
        modifier="h-full"
        size="small"
      />
    );
  }

  return (
    <Board
      header={<SectionTitle size="small" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex items-end">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
              {categoricalWithDriftCounter}

              <small>
                /
                {categoricalCounter}
              </small>
            </div>

          </div>

          <div>Categorical with drift</div>
        </div>
        )}
      modifier="h-full"
      size="small"
    />
  );
}

function NumericalFeaturesCounter() {
  const { data } = useGetCurrentDriftQueryWithPolling();

  const featureMetrics = data?.drift.featureMetrics ?? [];

  const numericalWithDriftCounter = featureMetrics.filter((feature) => feature.driftCalc.type === DRIFT_TEST_ENUM.KS && feature.driftCalc.hasDrift).length;
  const numericalCounter = featureMetrics.filter((feature) => feature.driftCalc.type === DRIFT_TEST_ENUM.KS).length;

  if (numericalCounter === 0) {
    return (
      <Board
        header={<SectionTitle size="small" />}
        main={(
          <div className="flex flex-col h-full items-center gap-4">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>--</div>

            <div>Numerical with drift</div>
          </div>
          )}
        modifier="h-full shadow"
        size="small"
      />
    );
  }

  return (
    <Board
      header={<SectionTitle size="small" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex items-center">
            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>
              {numericalWithDriftCounter}

              <small>
                /
                {numericalCounter}
              </small>
            </div>

          </div>

          <div>Numerical with drift</div>
        </div>
        )}
      modifier="h-full shadow"
      size="small"
    />
  );
}

export default DataDriftHeader;
