import { memo } from 'react';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import PieChart from '@Components/charts/pie-chart';
import SmartTable from '@Components/smart-table';
import { Spinner } from '@radicalbit/radicalbit-design-system';
import { NamespaceEnum } from '@Src/constants';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { getColumns } from './columns';

const { useGetOverallStatsQuery } = modelsApiSlice;

function ModelStatsList() {
  const { isLoading } = useGetOverallStatsQuery();

  if (isLoading) {
    <Spinner spinning />;
  }

  return (
    <div className="flex flex-col w-full h-full">
      <OverallCharts />

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

export default memo(ModelStatsList);
