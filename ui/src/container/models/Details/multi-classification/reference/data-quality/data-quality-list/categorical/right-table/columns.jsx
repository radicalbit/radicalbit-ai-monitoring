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
    width: '6rem',
    dataIndex: 'count',
  },
  {
    title: '',
    key: 'frequency',
    width: '5rem',
    align: 'right',
    render: ({ frequency }) => {
      const formattedFrequency = Math.floor(frequency * 100);
      return (
        <div>
          {formattedFrequency}
          %
        </div>
      );
    },
  },
  {
    title: 'Frequency',
    key: 'frequency',
    width: '12rem',
    render: ({ frequency }) => {
      const formattedFrequency = Math.floor(frequency * 100);
      return (
        <BarChart
          type="secondary"
          value={formattedFrequency}
          width="100%"
        />
      );
    },
  },
];

export default columns;
