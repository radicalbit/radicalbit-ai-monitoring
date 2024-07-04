import { useGetReferenceModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { DataTable } from '@radicalbit/radicalbit-design-system';
import columns from './columns.jsx';

function ClassTableMetrics() {
  const { data } = useGetReferenceModelQualityQueryWithPolling();
  const classMetrics = data?.modelQuality.classMetrics.map(({
    className, metrics: {
      precision, falsePositiveRate, recall, truePositiveRate, fMeasure,
    },
  }) => ({
    className,
    precision,
    falsePositiveRate,
    truePositiveRate,
    recall,
    fMeasure,
  })) ?? [];

  return (
    <DataTable
      columns={columns}
      dataSource={classMetrics}
      modifier="m-4"
      pagination={false}
      rowKey={({ label }) => label}
      scroll={{ y: '32rem' }}
      size="small"
    />
  );
}

export default ClassTableMetrics;
