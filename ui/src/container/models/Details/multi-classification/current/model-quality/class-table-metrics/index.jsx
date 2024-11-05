import {
  useGetCurrentDataQualityQueryWithPolling, useGetCurrentModelQualityQueryWithPolling, useGetReferenceDataQualityQueryWithPolling, useGetReferenceModelQualityQueryWithPolling,
} from '@State/models/polling-hook';
import { DataTable } from '@radicalbit/radicalbit-design-system';
import columns from './columns';

function ClassTableMetrics() {
  const { data: referenceData } = useGetReferenceModelQualityQueryWithPolling();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();

  const { data: referenceDataQuality } = useGetReferenceDataQualityQueryWithPolling();
  const { data: currentDataQuality } = useGetCurrentDataQualityQueryWithPolling();

  const referenceClassMetricsPredictions = referenceDataQuality?.dataQuality.classMetricsPrediction;
  const currentClassMetricsPredictions = currentDataQuality?.dataQuality.classMetricsPrediction;

  const currentClassMetrics = currentData?.modelQuality.classMetrics ?? [];
  const referenceClassMetrics = referenceData?.modelQuality.classMetrics ?? [];

  const classMetrics = currentClassMetrics.map((currentElement) => {
    const { className } = currentElement;

    const currentPrecision = currentElement?.metrics.precision;
    const currentRecall = currentElement?.metrics.recall;
    const currentfMeasure = currentElement?.metrics.fMeasure;
    const currentTruePositiveRate = currentElement?.metrics.truePositiveRate;
    const currentFalsePositiveRate = currentElement?.metrics.falsePositiveRate;

    const currentDataQualityElement = currentClassMetricsPredictions?.find((d) => d.name === className);
    const currentSupport = currentDataQualityElement?.count;
    const currentSupportPercent = currentDataQualityElement?.percentage;

    const referenceElement = referenceClassMetrics?.find((f) => f.className === className);
    const referencePrecision = referenceElement?.metrics.precision;
    const referenceRecall = referenceElement?.metrics.recall;
    const referencefMeasure = referenceElement?.metrics.fMeasure;
    const referenceTruePositiveRate = referenceElement?.metrics.truePositiveRate;
    const referenceFalsePositiveRate = referenceElement?.metrics.falsePositiveRate;

    const referenceDataQualityElement = referenceClassMetricsPredictions?.find((d) => d.name === className);
    const referenceSupport = referenceDataQualityElement?.count;
    const referenceSupportPercent = referenceDataQualityElement?.percentage;

    return {
      className,
      currentPrecision,
      currentRecall,
      currentfMeasure,
      currentTruePositiveRate,
      currentFalsePositiveRate,
      currentSupport,
      currentSupportPercent,
      referencePrecision,
      referenceRecall,
      referencefMeasure,
      referenceTruePositiveRate,
      referenceFalsePositiveRate,
      referenceSupport,
      referenceSupportPercent,
    };
  }) ?? [];

  return (
    <DataTable
      columns={columns}
      dataSource={classMetrics.sort((a, b) => a.className - b.className)}
      modifier="m-4"
      pagination={false}
      rowKey={({ label }) => label}
      scroll={{ y: '32rem' }}
      size="small"
    />
  );
}

export default ClassTableMetrics;
