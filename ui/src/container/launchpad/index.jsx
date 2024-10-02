import Right from './right';
import TopRow from './top-row';
import ModelStatsList from './central-row';

export default function Launchpad() {
  return (
    <div className="flex flex-col p-4 gap-4">
      <TopRow />

      <div className="grid grid-cols-[1.2fr,1.2fr,1fr,1.2fr] gap-4 h-full">
        <div className="col-span-3">
          <ModelStatsList />
        </div>

        <RightColumn />
      </div>
    </div>
  );
}

function RightColumn() {
  return (
    <Right />
  );
}
