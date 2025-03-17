import PieChart from '@Components/charts/pie-chart';
import SmartTable from '@Components/smart-table';
import { faBell } from '@fortawesome/free-solid-svg-icons';
import useModals from '@Hooks/use-modals';
import {
  Button,
  CustomLink,
  FontAwesomeIcon,
  NewHeader,
  SectionTitle,
  Skeleton,
  Void,
} from '@radicalbit/radicalbit-design-system';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetOverallModelListQueryWithPolling } from '@State/models/polling-hook';
import { memo } from 'react';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { alertsApiSlice } from '@State/alerts/api';
import { getColumns } from './columns';
import { getSkeletonColumns } from './skeleton-columns';

const { useGetOverallStatsQuery } = modelsApiSlice;
const { useGetAlertsQuery } = alertsApiSlice;

function ModelStatsList() {
  useGetOverallModelListQueryWithPolling();

  return (
    <div className="flex flex-col w-full">

      <OverallCharts />

      <AvailableModelHeader />

      <OverallList />

    </div>
  );
}

function OverallCharts() {
  const { data, isLoading } = useGetOverallStatsQuery();

  const dataQualityStats = data?.dataQuality || 0;
  const modelQualityStats = data?.modelQuality || 0;
  const dataDriftStats = data?.drift || 0;

  if (isLoading) {
    return (
      <div className="flex flex-row px-4">
        <OverallChartsSkeleton />

        <OverallChartsSkeleton />

        <OverallChartsSkeleton />
      </div>
    );
  }

  return (
    <div className="flex flex-row px-4 items-start justify-start ">
      <PieChart data={dataQualityStats} title="Data Quality" />

      <PieChart data={modelQualityStats} title="Model Quality" />

      <PieChart data={dataDriftStats} title="Drift Detection" />
    </div>
  );
}

function OverallChartsSkeleton() {
  return (
    <div className="flex flex-row items-center mx-6 gap-2 w-[14rem] h-[8rem]">
      <Skeleton.Avatar active size="large" />

      <div className="flex flex-col gap-2 w-full">
        <Skeleton.Input active block size="small" />

        <Skeleton.Input active block size="small" />
      </div>
    </div>
  );
}

function OverallList() {
  const { search } = useSearchParams();
  const navigate = useNavigate();

  const { data, isLoading } = useGetOverallModelListQueryWithPolling();
  const count = data?.length;

  const handleOnClick = ({ uuid }) => {
    navigate({ pathname: `/models/${uuid}`, search });
  };

  if (count === 0) {
    return (
      <div className="w-full h-[30rem] flex items-center">
        <AddNewModelVoid />
      </div>
    );
  }

  return (
    <SmartTable
      clickable
      columns={isLoading ? getSkeletonColumns : getColumns}
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

function AddNewModelVoid() {
  const { showModal } = useModals();

  const handleOnAddModel = () => {
    showModal(ModalsEnum.ADD_NEW_MODEL);
  };

  return (
    <Void
      actions={<Button onClick={handleOnAddModel} type="default">New Model</Button>}
      description={(
        <>
          Define and configure a new model
          <br />
          to begin monitoring its performance and gain insights.
        </>
      )}
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
  return (
    <NewHeader
      details={{
        one: (<AlertsButton />),
        two: (<AddNewModel />),
      }}
      title={<SectionTitle title="Available models" titleWeight="light" />}
    />
  );
}

function AlertsButton() {
  const { data = [] } = useGetAlertsQuery();
  const isActiveAlerts = data.length > 0;

  if (isActiveAlerts) {
    return (
      <CustomLink
        href="/launchpad#alert-table"
        title={(
          <Button
            className="p-2"
            onClick={() => {}}
            title="1"
            type="error"
          >
            <FontAwesomeIcon className="fa-shake" icon={faBell} size="xl" />
          </Button>
)}
      />
    );
  }
  return false;
}

export default memo(ModelStatsList);
