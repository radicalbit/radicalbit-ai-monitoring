import PieChart from '@Components/charts/pie-chart';
import TopRow from './top-row';

export default function Launchpad() {
  return (
    <div className="flex flex-col p-4 gap-8">
      <TopRow />

      <div className="grid grid-cols-4 h-full">
        <div className="col-span-3">
          <CentralSection />
        </div>

        <RightColumn />
      </div>
    </div>
  );
}

function CentralSection() {
  return (
    <div className="grid grid-rows-2">
      <OverallCharts />

      <OverallList />
    </div>

  );
}

function OverallCharts() {
  return (
    <div className="flex flex-row gap-16 items-start justify-start ">
      <PieChart currentData={84.3} referenceData={25} title="Data Quality" />

      <PieChart currentData={72.7} referenceData={40} title="Model Quality" />

      <PieChart currentData={92.3} referenceData={3.7} title="Drift Detection" />

    </div>
  );
}

function OverallList() {
  return (
    'TABLE'
  );
}

function RightColumn() {
  return (
    'RightColumn'
  );
}
