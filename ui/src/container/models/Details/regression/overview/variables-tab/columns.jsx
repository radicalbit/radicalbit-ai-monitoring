import { FEATURE_TYPE, OVERVIEW_ROW_TYPE } from '@Container/models/Details/constants';
import { useFormbitContext } from '@radicalbit/formbit';
import { Select, Tag } from '@radicalbit/radicalbit-design-system';
import useHandleOnSubmit from './useHandleOnSubmit';

const featuresColumns = (dataSource) => [
  {
    title: '#',
    key: 'index',
    width: '2rem',
    render: (_, record) => <span>{dataSource.indexOf(record) + 1}</span>,
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
    title: 'Field type',
    key: 'fieldType',
    dataIndex: 'fieldType',
    width: '10rem',
  },
  {
    title: 'Label',
    dataIndex: 'type',
    key: 'type',
    width: '15rem',
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

const featuresColumnsWithSelection = (dataSource) => [
  {
    title: '#',
    key: 'index',
    width: '2rem',
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
    title: 'Field type',
    key: 'fieldType',
    width: '10rem',
    onCell: () => ({ style: { height: '3.5rem' } }),
    render: (_, __, idx) => (<FieldTypeSelection variableIdx={idx} />),
  },
  {
    title: 'Label',
    dataIndex: 'type',
    key: 'type',
    width: '15rem',
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

const typeNotEditable = ['bool', 'string', 'datetime'];

function FieldTypeSelection({ variableIdx }) {
  const [, { isLoading }] = useHandleOnSubmit();

  const { form, write } = useFormbitContext();
  const variables = form?.variables;

  const fieldType = variables[variableIdx]?.fieldType;
  const type = variables[variableIdx]?.type;
  const rowType = variables[variableIdx]?.rowType;

  const options = [
    { label: 'numerical', value: FEATURE_TYPE.NUMERICAL },
    { label: 'categorical', value: FEATURE_TYPE.CATEGORICAL },
  ];

  const handleOnChange = (valueSelected) => {
    write(`variables[${variableIdx}]`, { ...variables[variableIdx], fieldType: valueSelected });
  };

  if (typeNotEditable.includes(`${type}`) || rowType !== '') {
    return fieldType;
  }

  return (
    <Select
      loading={isLoading}
      modifier="min-w-[15rem]"
      onChange={handleOnChange}
      options={options}
      readOnly={isLoading}
      value={fieldType}
    />
  );
}

export { featuresColumns, featuresColumnsWithSelection };
