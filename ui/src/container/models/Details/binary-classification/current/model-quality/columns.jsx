import { numberFormatter } from '@Src/constants';

export default [
  {
    title: <div className="font-[var(--coo-font-weight-bold)]">Metrics</div>,
    key: 'label',
    dataIndex: 'label',
    render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
  },
  {
    title: 'Current',
    key: 'currentValue',
    dataIndex: 'currentValue',
    align: 'right',
    render: (currentValue) => (currentValue) ? numberFormatter().format(currentValue) : '--',
  },
  {
    title: 'Reference',
    key: 'referenceValue',
    dataIndex: 'referenceValue',
    align: 'right',
    render: (referenceValue) => (referenceValue) ? numberFormatter().format(referenceValue) : '--',
  },

];
