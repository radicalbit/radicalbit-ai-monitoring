import Alerts from './alerts';
import WorkInProgress from './work-in-progress';

function Right() {
  return (
    <div className="flex flex-col gap-4 ml-4">
      <Alerts />

      <WorkInProgress />
    </div>
  );
}

export default Right;
