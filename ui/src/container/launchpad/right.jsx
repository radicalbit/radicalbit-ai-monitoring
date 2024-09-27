import { Board } from '@radicalbit/radicalbit-design-system';
import { alertsApiSlice } from '@Src/store/state/alerts/api';

const { useGetAlertsQuery } = alertsApiSlice;

function Right() {
  const { data = [undefined, undefined] } = useGetAlertsQuery();
  console.debug(data);

  return (
    <Board
      header="Alerts"
      main={(
        <div className="flex flex-col gap-2">
          {data.map((alert) => <Main alert={alert} />)}
        </div>
      )}
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

          {' '}

          <span>{fieldsInError}</span>
        </div>
      )}
      size="small"
      type="error"
    />
  );
}

export default Right;
