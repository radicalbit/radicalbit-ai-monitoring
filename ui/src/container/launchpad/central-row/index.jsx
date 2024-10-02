import PieChart from '@Components/charts/pie-chart';
import SmartTable from '@Components/smart-table';
import useModals from '@Hooks/use-modals';
import { Button, Spinner } from '@radicalbit/radicalbit-design-system';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { memo } from 'react';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { getColumns } from './columns';

const { useGetOverallStatsQuery } = modelsApiSlice;

function ModelStatsList() {
  const { isLoading } = useGetOverallStatsQuery();

  if (isLoading) {
    <Spinner spinning />;
  }

  return (
    <div className="flex flex-col w-full h-full">
      <div className="flex flex-row justify-between items-end">
        <OverallCharts />

        <AddNewModel />

      </div>

      <OverallList />
    </div>
  );
}

function OverallCharts() {
  const { data } = useGetOverallStatsQuery();

  const dataQualityStats = data?.overallStats.dataQuality;
  const modelQualityStats = data?.overallStats.modelQuality;
  const dataDriftStats = data?.overallStats.dataDrift;

  return (
    <div className="flex flex-row gap-16 items-start justify-start ">
      <PieChart data={dataQualityStats} title="Data Quality" />

      <PieChart data={modelQualityStats} title="Model Quality" />

      <PieChart data={dataDriftStats} title="Drift Detection" />

    </div>
  );
}

function OverallList() {
  const { search } = useSearchParams();
  const navigate = useNavigate();

  const { data } = useGetOverallStatsQuery();

  const modelStats = data?.modelStats.items;
  const count = data?.modelStats.count;

  const handleOnClick = ({ uuid }) => {
    navigate({ pathname: `/models/${uuid}`, search });
  };

  return (
    <SmartTable
      clickable
      columns={getColumns}
      dataSource={modelStats}
      fixedHeader="28rem"
      namespace={NamespaceEnum.MODELS_STATS}
      onRow={({ uuid }) => ({
        onClick: () => handleOnClick({ uuid }),
      })}
      recordCount={count}
      rowKey={({ uuid }) => uuid}
    />
  );
}

function AddNewModel() {
  const { showModal } = useModals();

  const onClick = () => {
    showModal(ModalsEnum.ADD_NEW_MODEL);
  };

  return (
    <Button modifier="mb-4" onClick={onClick} type="primary">
      New Model
    </Button>
  );
}

export default memo(ModelStatsList);
