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

    render: (data) => {
      const formattedFrequency = Math.floor(data.frequency * 100);
      const formattedReferenceFrequency = (data.referenceFrequency) ? Math.floor(data.referenceFrequency * 100) : 0;

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
    render: (data) => {
      const formattedFrequency = Math.floor(data.frequency * 100);
      const formattedReferenceFrequency = (data.referenceFrequency) ? Math.floor(data.referenceFrequency * 100) : 0;
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
