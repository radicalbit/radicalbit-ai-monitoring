import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { METRICS_TABS, MODEL_TABS_ENUM } from '@Container/models/Details/constants';
import { Board, SectionTitle, Skeleton } from '@radicalbit/radicalbit-design-system';
import { alertsApiSlice } from '@State/alerts/api';
import { useNavigate } from 'react-router';

const { useGetAlertsQuery } = alertsApiSlice;

function Alerts() {
  const { data = [], isLoading, isError } = useGetAlertsQuery();

  if (isLoading) {
    return (
      <Board
        header={<SectionTitle size="small" title="Alerts" />}
        main={(
          <div className="flex flex-col gap-2">
            <Skeleton.Input active block />

            <Skeleton.Input active block />

            <Skeleton.Input active block />
          </div>
      )}
      />
    );
  }

  if (isError) {
    return (
      <Board
        header={<SectionTitle size="small" title="Alerts" />}
        main={<SomethingWentWrong size="small" />}
        size="small"
      />
    );
  }

  return (
    <Board
      header={<SectionTitle size="small" title="Alerts" />}
      height="20rem"
      main={(
        <div className="flex flex-col gap-2">
          {data.map((alert) => (
            <Main alert={alert} />
          ))}
        </div>
      )}
      modifier="overflow-auto"
      size="small"
    />
  );
}

function Main({
  alert: {
    anomalyType, anomalyFeatures, modelUuid, modelName,
  },
}) {
  const navigate = useNavigate();

  const modelNametest = modelName ?? 'MODEL_NAME';
  const anomalyFeaturesJoined = anomalyFeatures.join(', ');
  const anomalyTypeLabel = METRICS_TABS[`${anomalyType}`] ?? 'SECTION';

  const handleOnClick = () => {
    navigate(`/models/${modelUuid}?tab=${MODEL_TABS_ENUM.CURRENT_DASHBOARD}&tab-metrics=${anomalyTypeLabel}`);
  };

  if (anomalyFeaturesJoined.length > 0) {
    return (
      <Board
        main={(
          <span>
            The
            {' '}

            <strong>{anomalyTypeLabel}</strong>

            {' '}

            of

            {' '}

            <strong>{modelNametest}</strong>

            {' '}

            model reports a problem on

            {' '}

            <strong>{anomalyFeaturesJoined}</strong>

            {' '}

            features
            .
          </span>
        )}
        onClick={handleOnClick}
        size="small"
        type="error"
      />
    );
  }

  return (
    <Board
      main={(
        <span>
          The

          {' '}

          <strong>{anomalyTypeLabel}</strong>

          {' '}

          of

          {' '}

          <strong>{modelNametest}</strong>

          {' '}

          model reports a problem
        </span>
      )}
      onClick={handleOnClick}
      size="small"
      type="error"
    />
  );
}

export default Alerts;
