import { useGetCurrentModelQualityQueryWithPolling, useGetReferenceModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { DataTable } from '@radicalbit/radicalbit-design-system';
import columns from './columns';

function ClassTableMetrics() {
  const { data: referenceData } = useGetReferenceModelQualityQueryWithPolling();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();

  const currentClassMetrics = currentData?.modelQuality.classMetrics ?? [];
  const referenceClassMetrics = referenceData?.modelQuality.classMetrics ?? [];

  const classMetrics = currentClassMetrics.map((currentElement) => {
    const { className } = currentElement;

    const currentPrecision = currentElement?.metrics.precision;
    const currentRecall = currentElement?.metrics.recall;
    const currentfMeasure = currentElement?.metrics.fMeasure;
    const currentTruePositiveRate = currentElement?.metrics.truePositiveRate;
    const currentFalsePositiveRate = currentElement?.metrics.falsePositiveRate;

    const referenceElement = referenceClassMetrics.find((f) => f.className === className);
    const referencePrecision = referenceElement?.metrics.precision;
    const referenceRecall = referenceElement?.metrics.recall;
    const referencefMeasure = referenceElement?.metrics.fMeasure;
    const referenceTruePositiveRate = referenceElement?.metrics.truePositiveRate;
    const referenceFalsePositiveRate = referenceElement?.metrics.falsePositiveRate;

    return {
      className,
      currentPrecision,
      currentRecall,
      currentfMeasure,
      currentTruePositiveRate,
      currentFalsePositiveRate,
      referencePrecision,
      referenceRecall,
      referencefMeasure,
      referenceTruePositiveRate,
      referenceFalsePositiveRate,
    };
  }) ?? [];

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

/*
 const { data: referenceData } = useGetReferenceModelQualityQueryWithPolling();
  console.debug('🚀 ~ ClassTableMetrics ~ referenceData:', referenceData);
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const referenceClassMetrics = referenceData?.modelQuality.classMetrics ?? [];
  console.debug('🚀 ~ ClassTableMetrics ~ referenceClassMetrics:', referenceData);
  const currentClassMetrics = currentData?.modelQuality.classMetrics ?? [];

  const classMetrics = currentClassMetrics.map(({
    className, metrics: {
      precision, falsePositiveRate, recall, truePositiveRate, fMeasure,
    },
  }) => {
    const referenceElement = referenceClassMetrics.find((f) => f.className === className);
    console.debug('🚀 ~ ClassTableMetrics ~ referenceElement:', referenceElement);
    return {
      className,
      currentPrecision: precision,
      currentFalsePositiveRate: falsePositiveRate,
      currentRecall: recall,
      currentTruePositiveRate: truePositiveRate,
      currentfMeasure: fMeasure,
      referencePrecision: referenceElement.precision,
      referenceFalsePositiveRate: referenceElement.falsePositiveRate,
      referenceRecall: referenceElement.recall,
      referenceTruePositiveRate: referenceElement.truePositiveRate,
      referencefMeasure: referenceElement.fMeasure,
    };
  }) ?? [];

*/