import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { useGetCurrentDriftQueryWithPolling } from '@State/models/polling-hook';
import { Board, SectionTitle } from '@radicalbit/radicalbit-design-system';

function DataDriftHeader() {
  return (
    <div className="flex gap-4">

      <TotalFeaturesCounter />

      <CategoricalFeaturesCounter />

      <NumericalFeaturesCounter />

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
        modifier="shadow basis-1/3"
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
      modifier="shadow basis-1/3"
      size="small"
      type="primary"
    />

  );
}

function CategoricalFeaturesCounter() {
  const { data } = useGetCurrentDriftQueryWithPolling();

  const featureMetrics = data?.drift.featureMetrics ?? [];
  const categoricalWithDriftCounter = featureMetrics.filter(({ fieldType, driftCalc }) => fieldType === FEATURE_TYPE.CATEGORICAL && driftCalc.some((d) => d.hasDrift)).length;
  const categoricalCounter = featureMetrics.filter(({ fieldType }) => fieldType === FEATURE_TYPE.CATEGORICAL).length;

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
        modifier="shadow basis-1/3"
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
      modifier="shadow basis-1/3"
      size="small"
    />
  );
}

function NumericalFeaturesCounter() {
  const { data } = useGetCurrentDriftQueryWithPolling();

  const featureMetrics = data?.drift.featureMetrics ?? [];

  const numericalWithDriftCounter = featureMetrics.filter(({ fieldType, driftCalc }) => fieldType === FEATURE_TYPE.NUMERICAL && driftCalc.some((d) => d.hasDrift)).length;
  const numericalCounter = featureMetrics.filter(({ fieldType }) => fieldType === FEATURE_TYPE.NUMERICAL).length;

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
        modifier="shadow basis-1/3"
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
      modifier="shadow basis-1/3"
      size="small"
    />
  );
}

export default DataDriftHeader;
