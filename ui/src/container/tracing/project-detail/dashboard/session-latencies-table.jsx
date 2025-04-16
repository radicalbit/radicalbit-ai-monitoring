import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { numberFormatter } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { DataTable, Skeleton } from '@radicalbit/radicalbit-design-system';
import isEmpty from 'lodash/isEmpty';
import { useParams } from 'react-router';
import { filtersToQueryParams } from './filters';

const {
  useGetSessionLatenciesQuery,
} = tracingApiSlice;

function SessionLatenciesTable() {
  const { uuid } = useParams();

  const { form } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;
  const toTimestamp = form?.toTimestamp;
  const skip = !fromTimestamp || !toTimestamp;
  const queryParams = filtersToQueryParams(fromTimestamp, toTimestamp);

  const {
    data = [], isSuccess, isLoading, isError,
  } = useGetSessionLatenciesQuery({ uuid, queryParams }, { skip });

  const pagination = data.length > 10 ? { pageSize: 10 } : false;

  if (isLoading) {
    return <Skeleton active paragraph={{ rows: 5 }} />;
  }

  if (isError) {
    return <SomethingWentWrong size="small" />;
  }

  if (isSuccess) {
    // e.g. 204 no content
    if (isEmpty(data)) {
      return (
        <DataTable
          columns={columns}
          dataSource={[]}
          pagination={pagination}
          size="small"
        />
      );
    }

    return (
      <DataTable
        columns={columns}
        dataSource={data}
        pagination={pagination}
        size="small"
      />
    );
  }

  if (data) {
    return (
      <DataTable
        columns={columns}
        dataSource={data}
        pagination={pagination}
        size="small"
      />
    );
  }

  return false;
}

const columns = [
  {
    title: 'Session UUID',
    dataIndex: 'sessionUuid',
    key: 'sessionUuid',
    width: '50%',
  },
  {
    title: '50th',
    dataIndex: 'p50Ms',
    key: 'p50Ms',
    render: (seconds) => {
      const formatted = numberFormatter().format(seconds);

      return `${formatted}ms`;
    },
  },
  {
    title: '90th',
    dataIndex: 'p90Ms',
    key: 'p90Ms',
    render: (seconds) => {
      const formatted = numberFormatter().format(seconds);

      return `${formatted}ms`;
    },
  },
  {
    title: '95th',
    dataIndex: 'p95Ms',
    key: 'p95Ms',
    render: (seconds) => {
      const formatted = numberFormatter().format(seconds);

      return `${formatted}ms`;
    },
  },
  {
    title: '99th',
    dataIndex: 'p99Ms',
    key: 'p99Ms',
    render: (seconds) => {
      const formatted = numberFormatter().format(seconds);

      return `${formatted}ms`;
    },
  },
];

export default SessionLatenciesTable;
