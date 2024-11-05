import { numberFormatter } from '@Src/constants';

export default [
  {
    title: '',
    key: 'label',
    dataIndex: 'label',
    render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
  },
  {
    title: 'Reference',
    key: 'value',
    dataIndex: 'value',
    align: 'right',
    render: (value) => numberFormatter().format(value),
  },
];
