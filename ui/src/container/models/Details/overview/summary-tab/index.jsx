import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCurrentImportsQueryWithPolling, useGetCurrentStatisticsQueryWithPolling, useGetReferenceStatisticsQueryWithPolling } from '@State/models/polling-hook';
import { modelsApiSlice } from '@Store/state/models/api';
import {
  Collapse,
  DataTable,
  Spinner,
} from '@radicalbit/radicalbit-design-system';
import moment from 'moment';
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

const { useGetCurrentStatisticsByUUIDQuery } = modelsApiSlice;

function SummaryTab() {
  const { data, isLoading } = useGetReferenceStatisticsQueryWithPolling();
  const jobStatus = data?.jobStatus;

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <>
        <ReferenceCurrentLatestComparison />

        <CurrentList />
      </>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function CurrentList() {
  const { data: currents } = useGetCurrentImportsQueryWithPolling();

  const [, ...rest] = currents?.items || [];

  if (rest.length === 0) {
    return false;
  }

  return (
    <Virtuoso
      className="mt-4"
      data={rest}
      itemContent={(_, { uuid: currentUUID }) => (<Currents currentUUID={currentUUID} />)}
      totalCount={rest.length}
    />
  );
}

function ReferenceCurrentLatestComparison() {
  const { data: reference, isSuccess: isReferenceSuccess } = useGetReferenceStatisticsQueryWithPolling();
  const date = reference?.date;

  const { data: latestCurrent } = useGetCurrentStatisticsQueryWithPolling();
  const latestStatistics = latestCurrent?.statistics;

  if (!isReferenceSuccess) {
    return false;
  }

  if (latestStatistics) {
    return (
      <Collapse
        collapsible="header"
        defaultActiveKey={date}
        expandIconPosition="end"
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
      modifier="p-4"
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
