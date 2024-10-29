import Alerts from './alerts';
import WorkInProgress from './work-in-progress';

function Right() {
  return (
    <div className="flex flex-col h-full gap-4 ml-4">
      <div className="min-h-[15rem] max-h-[16rem]">
        <WorkInProgress />

      </div>

      <div className="min-h-[15rem] h-full">
        <Alerts />

      </div>

    </div>
  );
}

export default Right;
