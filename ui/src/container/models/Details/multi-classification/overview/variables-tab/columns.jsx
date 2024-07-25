import { FEATURE_TYPE, OVERVIEW_ROW_TYPE } from '@Container/models/Details/constants';
import { useFormbitContext } from '@radicalbit/formbit';
import { Select, Tag } from '@radicalbit/radicalbit-design-system';

const featuresColumns = (dataSource) => [
  {
    title: '',
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
    render: (_, { rowType }, idx) => rowType === '' ? (<FieldTypeSelection variableIdx={idx} />) : false,
  },
  {
    title: '',
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

function FieldTypeSelection({ variableIdx }) {
  const { form, write } = useFormbitContext();
  const variables = form?.__metadata.variables;
  const variableFieldType = variables[variableIdx]?.fieldType;

  const options = [
    { label: 'Numerical', value: FEATURE_TYPE.NUMERICAL },
    { label: 'Categorical', value: FEATURE_TYPE.CATEGORICAL },
  ];

  const handleOnChange = (valueSelected) => {
    write(`__metadata.variables[${variableIdx}]`, { ...variables[variableIdx], fieldType: valueSelected });
  };

  return (<Select modifier="min-w-[15rem]" onChange={handleOnChange} options={options} value={variableFieldType} />
  );
}

export default featuresColumns;
