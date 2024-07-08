import { TABLE_COLOR } from '@Container/models/Details/constants';
import { numberFormatter } from '@Src/constants';
import { Truncate } from '@radicalbit/radicalbit-design-system';

export default [
  {
    title: '',
    key: 'className',
    dataIndex: 'className',
    onHeaderCell: () => ({ style: { background: 'transparent' } }),
    render: (label) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        <Truncate>
          {label}
        </Truncate>
      </div>
    ),
  },
  {
    title: () => (
      <div>
        Current
        <br />
        Precision
      </div>
    ),
    key: 'currentPrecision',
    dataIndex: 'currentPrecision',
    align: 'right',
    width: '5rem',
    onCell: () => ({ style: { background: `${TABLE_COLOR.CURRENT_COLUMN}` } }),
    onHeaderCell: () => ({ style: { background: `${TABLE_COLOR.CURRENT_COLUMN}` } }),
    render: (currentPrecision) => numberFormatter().format(currentPrecision),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        Precision
      </div>
    ),
    key: 'referencePrecision',
    dataIndex: 'referencePrecision',
    align: 'right',
    width: '5rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (referencePrecision) => numberFormatter().format(referencePrecision),
  },
  {
    title: () => (
      <div>
        Current
        <br />
        Recall
      </div>
    ),
    key: 'currentRecall',
    dataIndex: 'currentRecall',
    align: 'right',
    width: '4rem',
    onCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    render: (currentRecall) => numberFormatter().format(currentRecall),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        Recall
      </div>
    ),
    key: 'referenceRecall',
    dataIndex: 'referenceRecall',
    align: 'right',
    width: '4rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (referenceRecall) => numberFormatter().format(referenceRecall),
  },
  {
    title: () => (
      <div>
        Current
        <br />
        F1-Score
      </div>
    ),
    key: 'currentfMeasure',
    dataIndex: 'currentfMeasure',
    align: 'right',
    width: '5rem',
    onCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    render: (currentfMeasure) => numberFormatter().format(currentfMeasure),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        F1-Score
      </div>
    ),
    key: 'referencefMeasure',
    dataIndex: 'referencefMeasure',
    align: 'right',
    width: '5rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (referencefMeasure) => numberFormatter().format(referencefMeasure),
  },
  {
    title: () => (
      <div>
        Current
        <br />
        True Positive Rate
      </div>
    ),
    key: 'currentTruePositiveRate',
    dataIndex: 'currentTruePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    render: (currentTruePositiveRate) => numberFormatter().format(currentTruePositiveRate),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        True Positive Rate
      </div>
    ),
    key: 'referenceTruePositiveRate',
    dataIndex: 'referenceTruePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (referenceTruePositiveRate) => numberFormatter().format(referenceTruePositiveRate),
  },
  {
    title: () => (
      <div>
        Current
        <br />
        False Positive Rate
      </div>
    ),
    key: 'currentFalsePositiveRate',
    dataIndex: 'currentFalsePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    render: (currentFalsePositiveRate) => numberFormatter().format(currentFalsePositiveRate),
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        False Positive Rate
      </div>
    ),
    key: 'referenceFalsePositiveRate',
    dataIndex: 'referenceFalsePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: (referenceFalsePositiveRate) => numberFormatter().format(referenceFalsePositiveRate),
  },
  {
    title: () => (
      <div>
        Current
        <br />
        Support
      </div>
    ),
    key: 'currentSupport',

    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.CURRENT_COLUMN } }),
    render: ({ currentSupport, currentSupportPercent }) => `${numberFormatter().format(currentSupport)} (${numberFormatter().format(currentSupportPercent)}%)`,
  },
  {
    title: () => (
      <div>
        Reference
        <br />
        Support
      </div>
    ),
    key: 'referenceSupport',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    onHeaderCell: () => ({ style: { background: TABLE_COLOR.REFERENCE_COLUMN } }),
    render: ({ referenceSupport, referenceSupportPercent }) => `${numberFormatter().format(referenceSupport)} (${numberFormatter().format(referenceSupportPercent)}%)`,
  },
];
