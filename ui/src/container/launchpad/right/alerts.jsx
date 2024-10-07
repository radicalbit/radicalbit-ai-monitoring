import { Board, SectionTitle, Skeleton } from '@radicalbit/radicalbit-design-system';
import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { alertsApiSlice } from '@State/alerts/api';

const { useGetAlertsQuery } = alertsApiSlice;

function Alerts() {
  const { data = [undefined, undefined], isLoading, isError } = useGetAlertsQuery();
  console.debug(data);

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
      size="small"
    />
  );
}

function Main({ alert }) {
  const alertType = alert?.alertType || 'Foo';
  const fieldsInError = alert?.fieldsInError || 'Bar';

  return (
    <Board
      borderType="none"
      main={(
        <div>
          <strong>{alertType}</strong>

          <span>{fieldsInError}</span>
        </div>
      )}
      size="small"
      type="error"
    />
  );
}

export default Alerts;
