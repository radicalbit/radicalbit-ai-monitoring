import { Tag } from '@radicalbit/radicalbit-design-system';
import { OVERVIEW_ROW_TYPE } from '@Container/models/Details/constants';

const outputsColumns = (dataSource) => [
  {
    title: '#',
    key: 'index',
    width: '30px',
    render: (_, record) => <span>{dataSource.indexOf(record) + 1}</span>,
  }, {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  }, {
    title: 'Type',
    dataIndex: 'type',
    key: 'type',
  }, {
    title: 'Label',
    dataIndex: 'outputType',
    key: 'outputType',
    align: 'right',
    render: (_, record) => {
      if (record.outputType.length > 0) {
        const tagType = record.outputType === OVERVIEW_ROW_TYPE.PREDICTION ? 'full' : '';
        return (
          <div className="flex justify-end">
            <Tag type={tagType}>{record.outputType}</Tag>
          </div>
        );
      }

      return false;
    },
  },
];
export default outputsColumns;
