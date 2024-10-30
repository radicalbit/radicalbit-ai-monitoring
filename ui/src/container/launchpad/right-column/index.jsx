import { alertsApiSlice } from '@Src/store/state/alerts/api';
import Alerts from './alerts';
import WorkInProgress from './work-in-progress';

const { useGetAlertsQuery } = alertsApiSlice;

function RightColumn() {
  const { data = [] } = useGetAlertsQuery();
  const count = data?.length;

  if (count === 0) {
    return (
      <div className="flex flex-col h-full gap-4 ml-4">
        <WorkInProgress />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full gap-4 ml-4">
      <div className="max-h-[16rem] h-full">
        <WorkInProgress />

      </div>

      <div className="min-h-[15rem] h-full">
        <Alerts />

      </div>

    </div>
  );
}

export default RightColumn;
