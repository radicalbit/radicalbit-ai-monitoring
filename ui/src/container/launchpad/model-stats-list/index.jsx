import PieChart from '@Components/charts/pie-chart';
import SmartTable from '@Components/smart-table';
import { faBell } from '@fortawesome/free-solid-svg-icons';
import useModals from '@Hooks/use-modals';
import {
  Button,
  FontAwesomeIcon,
  NewHeader,
  SectionTitle,
  Skeleton,
  Void,
} from '@radicalbit/radicalbit-design-system';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { useGetOverallModelListQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { memo } from 'react';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { getColumns } from './columns';

const { useGetOverallStatsQuery } = modelsApiSlice;

function ModelStatsList() {
  useGetOverallModelListQueryWithPolling();
  const { isLoading } = useGetOverallStatsQuery();

  if (isLoading) {
    return (
      <Skeleton active block className="my-8" paragraph={{ rows: 5, width: '100%' }} title={{ width: '100%' }} />
    );
  }

  return (
    <div className="flex flex-col w-full">

      <OverallCharts />

      <AvailableModelHeader />

      <OverallList />

    </div>
  );
}

function OverallCharts() {
  const { data } = useGetOverallStatsQuery();
  const dataQualityStats = data?.dataQuality || 0;
  const modelQualityStats = data?.modelQuality || 0;
  const dataDriftStats = data?.drift || 0;

  return (
    <div className="flex flex-row px-4 items-start justify-start ">
      <PieChart data={dataQualityStats} title="Data Quality" />

      <PieChart data={modelQualityStats} title="Model Quality" />

      <PieChart data={dataDriftStats} title="Drift Detection" />

    </div>
  );
}

function OverallList() {
  const { search } = useSearchParams();
  const navigate = useNavigate();

  const { data } = useGetOverallModelListQueryWithPolling();
  const count = data?.length;

  const handleOnClick = ({ uuid }) => {
    navigate({ pathname: `/models/${uuid}`, search });
  };

  if (count === 0) {
    return (
      <Void
        actions={<AddNewModel />}
        description="No models are available."
      />
    );
  }

  return (
    <SmartTable
      clickable
      columns={getColumns}
      dataSource={data}
      fixedHeader="30rem"
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
    <Button onClick={onClick} type="primary">
      New Model
    </Button>
  );
}

function AvailableModelHeader() {
  const navigate = useNavigate();
  const handleOnClick = () => {
    navigate('#alert-table');
  };

  return (
    <NewHeader
      details={{
        one: (
          <Button
            className="p-2"
            onClick={handleOnClick}
            title="1"
            type="error"
          >
            <FontAwesomeIcon className="fa-shake" icon={faBell} size="xl" />
          </Button>
        ),
        two: (
          <AddNewModel />
        ),

      }}
      title={<SectionTitle title="Available models" titleWeight="light" />}
    />
  );
}

export default memo(ModelStatsList);
