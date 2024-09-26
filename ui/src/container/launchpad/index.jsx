import TopRow from './top-row';

export default function Launchpad() {
  return (
    <div className="grid grid-rows-2 p-4 gap-8">
      <TopRow />

      <CentralRow />
    </div>
  );
}

function CentralRow() {
  return (
    <div className="grid grid-cols-4 h-full">
      <div className="col-span-3">
        <CentralTable />
      </div>

      <RightColumn />
    </div>
  );
}

function CentralTable() {
  return (
    'CentralTable'
  );
}

function RightColumn() {
  return (
    'RightColumn'
  );
}
