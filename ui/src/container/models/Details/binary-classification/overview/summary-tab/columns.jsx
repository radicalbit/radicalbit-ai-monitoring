import { numberFormatter } from '@Src/constants';

const currentColumns = [{
  title: '',
  key: 'label',
  dataIndex: 'label',
  render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
}, {
  title: 'Current',
  key: 'currentValue',
  dataIndex: 'currentValue',
  align: 'right',
  render: (value) => numberFormatter().format(value),
}];

const referenceColumns = [{
  title: '',
  key: 'label',
  dataIndex: 'label',
  render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
}, {
  title: 'Reference',
  key: 'referenceValue',
  dataIndex: 'referenceValue',
  align: 'right',
  render: (value) => numberFormatter().format(value),
}];

const columnsComparison = [{
  title: '',
  key: 'label',
  dataIndex: 'label',
  render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
},
{
  title: 'Current',
  key: 'currentValue',
  dataIndex: 'currentValue',
  align: 'right',
  render: (currentValue) => numberFormatter().format(currentValue),
},
{
  title: 'Reference',
  key: 'referenceValue',
  dataIndex: 'referenceValue',
  align: 'right',
  render: (referenceValue) => numberFormatter().format(referenceValue),
}];

const leftDataSourceTable = ({ reference, current }) => [
  {
    label: 'Number of fields',
    referenceValue: reference ? reference.statistics.nVariables : undefined,
    currentValue: current ? current.statistics?.nVariables : undefined,
  },
  {
    label: 'Number of observations',
    referenceValue: reference ? reference.statistics.nObservations : undefined,
    currentValue: current ? current.statistics?.nObservations : undefined,
  },
  {
    label: 'Missing values',
    referenceValue: reference ? reference.statistics.missingCells : undefined,
    currentValue: current ? current.statistics?.missingCells : undefined,
  },
  {
    label: 'Missing values (%)',
    referenceValue: reference ? reference.statistics.missingCellsPerc : undefined,
    currentValue: current ? current.statistics?.missingCellsPerc : undefined,
  },
  {
    label: 'Duplicated rows',
    referenceValue: reference ? reference.statistics.duplicateRows : undefined,
    currentValue: current ? current.statistics?.duplicateRows : undefined,
  },
  {
    label: 'Duplicated rows (%)',
    referenceValue: reference ? reference.statistics.duplicateRowsPerc : undefined,
    currentValue: current ? current.statistics?.duplicateRowsPerc : undefined,
  },
];

const rigthDataSourceTable = ({ reference, current }) => [
  {
    label: 'Numerical',
    referenceValue: reference ? reference.statistics.numeric : undefined,
    currentValue: current ? current.statistics?.numeric : undefined,
  },
  {
    label: 'Categorical',
    referenceValue: reference ? reference.statistics.categorical : undefined,
    currentValue: current ? current.statistics?.categorical : undefined,
  },
  {
    label: 'Datetime',
    referenceValue: reference ? reference.statistics.datetime : undefined,
    currentValue: current ? current.statistics?.datetime : undefined,
  },
];

export {
  currentColumns,
  referenceColumns,
  columnsComparison,
  leftDataSourceTable,
  rigthDataSourceTable,
};
