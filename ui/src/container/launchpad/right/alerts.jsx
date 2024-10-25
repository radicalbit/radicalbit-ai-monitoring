import { Board, SectionTitle, Skeleton } from '@radicalbit/radicalbit-design-system';
import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { alertsApiSlice } from '@State/alerts/api';

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
      main={(
        <div className="flex flex-col gap-2">
          {data.map((alert) => (
            <Main alert={alert} />
          ))}
        </div>
      )}
      modifier="min-h-[20vh]"
      size="small"
    />
  );
}

function Main({ alert }) {
  const anomalyType = alert?.anomalyType;
  const anomalyFeatures = alert?.anomalyFeatures;

  return (
    <Board
      borderType="none"
      main={(
        <div>
          <strong>{anomalyType}</strong>

          {anomalyFeatures.map((anomalyFeature) => (<span>{anomalyFeature}</span>))}

        </div>
      )}
      size="small"
      type="error"
    />
  );
}

export default Alerts;
