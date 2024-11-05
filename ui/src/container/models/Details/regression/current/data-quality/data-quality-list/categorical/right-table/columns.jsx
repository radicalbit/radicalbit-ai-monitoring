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
    render: ({ frequency, referenceFrequency }) => {
      const formattedFrequency = Math.floor(frequency * 100);
      const formattedReferenceFrequency = (referenceFrequency) ? Math.floor(referenceFrequency * 100) : 0;
      return (
        <div className="flex flex-col items-end gap-1">
          <div>
            {formattedReferenceFrequency}
            %
          </div>

          <div>
            {formattedFrequency}
            %
          </div>
        </div>
      );
    },

  },
  {
    title: 'Frequency',
    key: 'frequency',
    width: '12rem',
    render: ({ frequency, referenceFrequency }) => {
      const formattedFrequency = Math.floor(frequency * 100);
      const formattedReferenceFrequency = (referenceFrequency) ? Math.floor(referenceFrequency * 100) : 0;
      return (
        <div className="flex flex-col gap-2">
          <BarChart
            type="secondary"
            value={formattedReferenceFrequency}
            width="100%"
          />

          <BarChart
            type="primary"
            value={formattedFrequency}
            width="100%"
          />
        </div>
      );
    },

  },
];

export default columns;
