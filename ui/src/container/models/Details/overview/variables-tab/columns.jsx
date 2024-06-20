import { Tag } from '@radicalbit/radicalbit-design-system';

const featuresColumns = (dataSource) => [
  {
    title: '',
    key: 'index',
    width: '30px',
    render: (_, record) => <label>{dataSource.indexOf(record) + 1}</label>,
  }, {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  }, {
    title: 'Type',
    dataIndex: 'type',
    key: 'type',
  },
  {
    title: '',
    dataIndex: 'type',
    key: 'type',
    render: (_, record) => {
      if (record.rowType) {
        return (
          <div className="flex justify-end">
            <Tag type="full">{record.rowType}</Tag>
          </div>
        );
      }
      return false;
    },
  },
];

export default featuresColumns;
