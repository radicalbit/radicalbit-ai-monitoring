import { BarChart } from '@radicalbit/radicalbit-design-system';

const columns = [
  {
    title: 'Name',
    key: 'name',
    dataIndex: 'name',
  },
  {
    title: 'Count',
    key: 'count',
    width: '8rem',
    dataIndex: 'count',
  },
  {
    title: '',
    key: 'frequency',
    width: '8rem',

    render: ({ frequency, referenceFrequency }) => (
      <div className="flex flex-col items-end gap-1">
        <div>
          {referenceFrequency}
          %
        </div>

        <div>
          {frequency}
          %
        </div>
      </div>
    ),
  },
  {
    title: 'Frequency',
    key: 'frequency',
    width: '12rem',
    render: ({ frequency, referenceFrequency }) => (
      <div className="flex flex-col gap-2">
        <BarChart
          type="secondary"
          value={referenceFrequency}
          width="100%"
        />

        <BarChart
          type="primary"
          value={frequency}
          width="100%"
        />
      </div>
    ),
  },
];

export default columns;
