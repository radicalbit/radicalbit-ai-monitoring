import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { numberFormatter } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { DataTable, Skeleton } from '@radicalbit/radicalbit-design-system';
import isEmpty from 'lodash/isEmpty';
import { useParams } from 'react-router-dom';
import { filtersToQueryParams } from './filters';

const {
  useGetTraceLatenciesQuery,
} = tracingApiSlice;

function TraceLatenciesTable() {
  const { uuid } = useParams();

  const { form } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;
  const toTimestamp = form?.toTimestamp;
  const queryParams = filtersToQueryParams(fromTimestamp, toTimestamp);
  const skip = !fromTimestamp || !toTimestamp;

  const pagination = false;

  const {
    data, isSuccess, isLoading, isError,
  } = useGetTraceLatenciesQuery({ uuid, queryParams }, { skip });

  if (isLoading) {
    return <Skeleton active paragraph={{ rows: 2 }} />;
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
        dataSource={[data]}
        pagination={pagination}
        size="small"
      />
    );
  }

  if (data) {
    return (
      <DataTable
        columns={columns}
        dataSource={[data]}
        pagination={pagination}
        size="small"
      />
    );
  }

  return false;
}

const columns = [
  {
    title: '',
    dataIndex: 'witdh',
    key: 'witdh',
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

export default TraceLatenciesTable;
