import { numberFormatter } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { DataTable } from '@radicalbit/radicalbit-design-system';

const {
  useGetSessionLatenciesQuery,
} = tracingApiSlice;

function SessionLatenciesTable() {
  const { data, isSuccess } = useGetSessionLatenciesQuery();

  if (isSuccess) {
    return (
      <DataTable
        columns={columns}
        dataSource={data}
      />
    );
  }

  return false;
}

const columns = [
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
