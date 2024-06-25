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
    title: 'Frequency (%)',
    key: 'frequency',
    width: '12rem',
    render: ({ frequency }) => {
      const formattedFrequency = Math.floor(frequency * 100);
      return (
        <BarChart
          content={`${formattedFrequency}%`}
          type="secondary"
          value={formattedFrequency}
          width="100%"
        />
      );
    },
  },
];

export default columns;
