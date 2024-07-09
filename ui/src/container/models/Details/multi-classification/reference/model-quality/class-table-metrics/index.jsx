import { useGetReferenceDataQualityQueryWithPolling, useGetReferenceModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { DataTable } from '@radicalbit/radicalbit-design-system';
import columns from './columns';

function ClassTableMetrics() {
  const { data: modelQualityData } = useGetReferenceModelQualityQueryWithPolling();
  const { data: dataQuality } = useGetReferenceDataQualityQueryWithPolling();

  const dataQualityData = dataQuality?.dataQuality.classMetricsPrediction;

  const classMetrics = modelQualityData?.modelQuality?.classMetrics.map(({
    className, metrics: {
      precision, falsePositiveRate, recall, truePositiveRate, fMeasure,
    },
  }) => {
    const classMetricsPrediction = dataQualityData.find((d) => d.name === className);
    return {
      className,
      precision,
      falsePositiveRate,
      truePositiveRate,
      recall,
      fMeasure,
      support: classMetricsPrediction?.count,
      supportPercent: classMetricsPrediction?.percentage,
    };
  }).sort((a, b) => a.className - b.className) ?? [];

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
