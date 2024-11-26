import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import SmartTable from '@Components/smart-table';
import { METRICS_TABS, MODEL_TABS_ENUM } from '@Container/models/Details/constants';
import {
  DataTable,
  SectionTitle, Skeleton, NewHeader,
} from '@radicalbit/radicalbit-design-system';
import { NamespaceEnum } from '@Src/constants';
import { alertsApiSlice } from '@State/alerts/api';
import { useNavigate } from 'react-router';
import { getColumns } from './columns';
import { getSkeletonColumns } from './skeleton-columns';

const { useGetAlertsQuery } = alertsApiSlice;

function AlertList() {
  const navigate = useNavigate();
  const { data = [], isLoading, isError } = useGetAlertsQuery();
  const count = data?.length;

  const handleOnClick = ({ modelUuid, anomalyType }) => {
    navigate(`/models/${modelUuid}?tab=${MODEL_TABS_ENUM.CURRENT_DASHBOARD}&tab-metrics=${METRICS_TABS[`${anomalyType}`]}`);
  };

  if (isError) {
    return (
      <div className="flex flex-col justify-start">
        <NewHeader
          title={<SectionTitle title="Alert" titleWeight="light" />}
        />

        <SomethingWentWrong size="small" />
      </div>

    );
  }

  if (count === 0) {
    return false;
  }

  return (
    <div className="flex flex-col justify-start" id="alert-table">
      <NewHeader
        title={<SectionTitle id="alert-table" title="Alert" titleWeight="light" />}
      />

      <SmartTable
        clickable
        columns={isLoading ? getSkeletonColumns : getColumns}
        dataSource={data}
        fixedHeader="30rem"
        namespace={NamespaceEnum.ALERTS}
        onRow={({ modelUuid, anomalyType }) => ({
          onClick: () => handleOnClick({ modelUuid, anomalyType }),
        })}
        recordCount={count}
        rowClassName={isLoading ? '' : DataTable.ROW_ERROR}
        rowKey={({ uuid }) => uuid}
      />
    </div>
  );
}

export default AlertList;
