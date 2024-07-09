import { TABLE_COLOR } from '@Container/models/Details/constants';
import { numberFormatter } from '@Src/constants';

export default [
  {
    title: '',
    key: 'className',
    dataIndex: 'className',
    render: (label) => <div className="font-[var(--coo-font-weight-bold)]">{label}</div>,
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        Precison
      </div>
    ),
    key: 'precision',
    dataIndex: 'precision',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (precision) => numberFormatter().format(precision),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        Recall
      </div>
    ),
    key: 'recall',
    dataIndex: 'recall',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (recall) => numberFormatter().format(recall),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        F1-Score
      </div>
    ),
    key: 'fMeasure',
    dataIndex: 'fMeasure',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (fMeasure) => numberFormatter().format(fMeasure),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        True Positive Rate
      </div>
    ),
    key: 'truePositiveRate',
    dataIndex: 'truePositiveRate',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (truePositiveRate) => numberFormatter().format(truePositiveRate),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        False Positive Rate
      </div>
    ),
    key: 'falsePositiveRate',
    dataIndex: 'falsePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (falsePositiveRate) => numberFormatter().format(falsePositiveRate),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        Support
      </div>
    ),
    key: 'support',
    align: 'right',
    width: '10rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: ({ support, supportPercent }) => `${numberFormatter().format(support)} (${numberFormatter().format(supportPercent)}%)`,
  },
];
