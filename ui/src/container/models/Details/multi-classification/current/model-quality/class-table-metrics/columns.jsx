import { CHART_COLOR } from '@Helpers/common-chart-options';
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
    title: 'Precision',
    key: 'currentPrecision',
    dataIndex: 'currentPrecision',
    align: 'right',
    width: '5rem',
    onCell: () => ({ style: { background: `${CHART_COLOR.CURRENT_LIGHT}` } }),
    onHeaderCell: () => ({ style: { background: `${CHART_COLOR.CURRENT_LIGHT}` } }),
    render: (currentPrecision) => numberFormatter().format(currentPrecision),
  },
  {
    title: 'Precision',
    key: 'referencePrecision',
    dataIndex: 'referencePrecision',
    align: 'right',
    width: '5rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (referencePrecision) => numberFormatter().format(referencePrecision),
  },
  {
    title: 'Recall',
    key: 'currentRecall',
    dataIndex: 'currentRecall',
    align: 'right',
    width: '4rem',
    onCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    render: (currentRecall) => numberFormatter().format(currentRecall),
  },
  {
    title: 'Recall',
    key: 'referenceRecall',
    dataIndex: 'referenceRecall',
    align: 'right',
    width: '4rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (referenceRecall) => numberFormatter().format(referenceRecall),
  },
  {
    title: 'F1-Score',
    key: 'currentfMeasure',
    dataIndex: 'currentfMeasure',
    align: 'right',
    width: '6rem',
    onCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    render: (currentfMeasure) => numberFormatter().format(currentfMeasure),
  },
  {
    title: 'F1-Score',
    key: 'referencefMeasure',
    dataIndex: 'referencefMeasure',
    align: 'right',
    width: '6rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (referencefMeasure) => numberFormatter().format(referencefMeasure),
  },
  {
    title: 'True Positive Rate',
    key: 'currentTruePositiveRate',
    dataIndex: 'currentTruePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    render: (currentTruePositiveRate) => numberFormatter().format(currentTruePositiveRate),
  },
  {
    title: 'True Positive Rate',
    key: 'referenceTruePositiveRate',
    dataIndex: 'referenceTruePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (referenceTruePositiveRate) => numberFormatter().format(referenceTruePositiveRate),
  },
  {
    title: 'False Positive Rate',
    key: 'currentFalsePositiveRate',
    dataIndex: 'currentFalsePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.CURRENT_LIGHT } }),
    render: (currentFalsePositiveRate) => numberFormatter().format(currentFalsePositiveRate),
  },
  {
    title: 'False Positive Rate',
    key: 'referenceFalsePositiveRate',
    dataIndex: 'referenceFalsePositiveRate',
    align: 'right',
    width: '8rem',
    onCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    onHeaderCell: () => ({ style: { background: CHART_COLOR.REFERENCE_LIGHT } }),
    render: (referenceFalsePositiveRate) => numberFormatter().format(referenceFalsePositiveRate),
  },
];
