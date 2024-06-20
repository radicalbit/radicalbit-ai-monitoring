import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetReferenceStatisticsQueryWithPolling } from '@State/models/polling-hook';
import { modelsApiSlice } from '@Store/state/models/api';
import moment from 'moment';
import {
  Collapse,
  DataTable,
  Spinner,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';
import { Virtuoso } from 'react-virtuoso';
import {
  columnsComparison,
  currentColumns,
  leftDataSourceTable,
  referenceColumns,
  rigthDataSourceTable,
} from './columns';

const { Panel } = Collapse;
const {
  useGetReferenceStatisticsQuery,
  useGetCurrentImportsQuery,
  useGetCurrentStatisticsByUUIDQuery,
  useGetCurrentStatisticsLatestQuery,
} = modelsApiSlice;

function SummaryTab() {
  const { uuid } = useParams();

  useGetReferenceStatisticsQueryWithPolling();

  const { data } = useGetReferenceStatisticsQuery({ uuid });

  const { data: currents } = useGetCurrentImportsQuery({ uuid });

  const [, ...rest] = currents?.items || [];

  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <Spinner>
        <ReferenceCurrentLatestComparison />

        <Virtuoso
          className="mt-4"
          data={rest}
          itemContent={(_, { uuid: currentUUID }) => (<Currents currentUUID={currentUUID} />)}
          totalCount={rest.length}
        />
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function ReferenceCurrentLatestComparison() {
  const { uuid } = useParams();

  const { data: reference, isSuccess: isReferenceSuccess } = useGetReferenceStatisticsQuery({ uuid });
  const date = reference?.date;

  const { data: latestCurrent, isSuccess: isLatestCurrentSuccess } = useGetCurrentStatisticsLatestQuery({ uuid });
  const latestStatistics = latestCurrent?.statistics;

  if (!isReferenceSuccess || !isLatestCurrentSuccess) {
    return false;
  }

  if (latestStatistics) {
    return (
      <Collapse
        collapsible="header"
        defaultActiveKey={date}
        expandIconPosition="end"
        modifier="pb-4 mt-4"
        type="primary-light"
      >
        <Panel key={date} header="Reference vs current overview">
          <div className="flex flex-row gap-4">
            <DataTable
              columns={columnsComparison}
              dataSource={leftDataSourceTable({ reference, current: latestCurrent })}
              modifier="basis-1/2"
              pagination={false}
              rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
              rowKey={({ label }) => label}
              size="small"
            />

            <DataTable
              columns={columnsComparison}
              dataSource={rigthDataSourceTable({ reference, current: latestCurrent })}
              modifier="basis-1/2"
              pagination={false}
              rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
              rowKey={({ label }) => label}
              size="small"
            />
          </div>
        </Panel>
      </Collapse>
    );
  }

  return (
    <Collapse
      collapsible="header"
      defaultActiveKey={date}
      expandIconPosition="end"
      modifier="pb-4 mt-4"
      type="secondary-medium"
    >
      <Panel key={date} header="Reference overview">
        <div className="flex flex-row gap-4">
          <DataTable
            columns={referenceColumns}
            dataSource={leftDataSourceTable({ reference })}
            modifier="basis-1/2"
            pagination={false}
            rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
            rowKey={({ label }) => label}
            size="small"
          />

          <DataTable
            columns={referenceColumns}
            dataSource={rigthDataSourceTable({ reference })}
            modifier="basis-1/2"
            pagination={false}
            rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
            rowKey={({ label }) => label}
            size="small"
          />
        </div>
      </Panel>
    </Collapse>
  );
}

function Currents({ currentUUID }) {
  const { uuid } = useParams();

  const { data: current, isSuccess } = useGetCurrentStatisticsByUUIDQuery({ uuid, currentUUID });
  const date = current?.date;

  if (!isSuccess) {
    return false;
  }

  return (
    <Collapse
      collapsible="header"
      expandIconPosition="end"
      modifier="pb-4"
    >
      <Panel key={date} header={`Current - ${moment(date).format('YYYY.MM.DD HH.mm')}`}>
        <div className="flex flex-row gap-4">
          <DataTable
            columns={currentColumns}
            dataSource={leftDataSourceTable({ current })}
            modifier="basis-1/2"
            pagination={false}
            rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
            rowKey={({ label }) => label}
            size="small"
          />

          <DataTable
            columns={currentColumns}
            dataSource={rigthDataSourceTable({ current })}
            modifier="basis-1/2"
            pagination={false}
            rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
            rowKey={({ label }) => label}
            size="small"
          />
        </div>
      </Panel>
    </Collapse>
  );
}

export default SummaryTab;
