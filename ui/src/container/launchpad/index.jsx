import Right from './right';

export default function Launchpad() {
  return (
    <div className="grid grid-rows-2">
      <TopRow />

      <CentralRow />
    </div>
  );
}

function TopRow() {
  return (
    <div className="grid grid-cols-4">

      <div className="">1</div>

      <div className="">2</div>

      <div className="">3</div>

      <div className="">4</div>
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
    <Right />
  );
}
