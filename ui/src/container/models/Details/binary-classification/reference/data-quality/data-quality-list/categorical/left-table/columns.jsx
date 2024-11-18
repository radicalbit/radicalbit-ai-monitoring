const columns = [
  {
    title: 'Label',
    key: 'label',
    dataIndex: 'label',
    render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
  },
  {
    title: 'Value',
    key: 'value',
    dataIndex: 'value',
    align: 'right',
  },
];

export default columns;
