import { OVERVIEW_ROW_TYPE } from '@Container/models/Details/constants';
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
    render: (_, { rowType }) => {
      if (rowType) {
        const tagType = rowType === OVERVIEW_ROW_TYPE.GROUND_TRUTH ? 'full' : rowType === OVERVIEW_ROW_TYPE.TIMESTAMP ? 'light' : '';
        return (
          <div className="flex justify-end">
            <Tag type={tagType}>{rowType}</Tag>
          </div>
        );
      }
      return false;
    },
  },
];

export default featuresColumns;
