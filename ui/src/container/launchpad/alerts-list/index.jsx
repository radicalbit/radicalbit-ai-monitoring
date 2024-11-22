import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import SmartTable from '@Components/smart-table';
import { METRICS_TABS, MODEL_TABS_ENUM } from '@Container/models/Details/constants';
import {
  DataTable,
  SectionTitle, Skeleton,
} from '@radicalbit/radicalbit-design-system';
import { NamespaceEnum } from '@Src/constants';
import { alertsApiSlice } from '@State/alerts/api';
import { useNavigate } from 'react-router';
import { getColumns } from './columns';

const { useGetAlertsQuery } = alertsApiSlice;

function AlertList() {
  const navigate = useNavigate();
  const { data = [], isLoading, isError } = useGetAlertsQuery();
  const count = data?.length;

  const handleOnClick = ({ modelUuid, anomalyType }) => {
    navigate(`/models/${modelUuid}?tab=${MODEL_TABS_ENUM.CURRENT_DASHBOARD}&tab-metrics=${METRICS_TABS[`${anomalyType}`]}`);
  };

  if (isLoading) {
    return (
      <div className="flex flex-col gap-9 justify-start">
        <SectionTitle title="Alert" titleWeight="light" />

        <Skeleton.Input active block />
      </div>

    );
  }

  if (isError) {
    return (
      <div className="flex flex-col gap-9 justify-start">
        <SectionTitle title="Alert" titleWeight="light" />

        <SomethingWentWrong size="small" />
      </div>

    );
  }

  if (count === 0) {
    return false;
  }

  return (
    <div className="flex flex-col gap-9 justify-start">
      <SectionTitle id="alert-table" title="Alert" titleWeight="light" />

      <SmartTable
        clickable
        columns={getColumns}
        dataSource={data}
        fixedHeader="30rem"
        namespace={NamespaceEnum.ALERTS}
        onRow={({ modelUuid, anomalyType }) => ({
          onClick: () => handleOnClick({ modelUuid, anomalyType }),
        })}
        recordCount={count}
        rowClassName={DataTable.ROW_ERROR}
        rowKey={({ uuid }) => uuid}
      />
    </div>
  );
}

export default AlertList;
