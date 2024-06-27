import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import ConfusionMatrix from '@Container/models/Details/charts/confusion-matrix-chart';
import { CHART_COLOR, MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import {
  Board, DataTable, SectionTitle, Spinner,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { useParams } from 'react-router';
import { useGetCurrentModelQualityLatestQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { useGetCurrentModelQuality } from '@State/models/modal-hook';
import {
  AccuracyChart, AreaUnderPrChart, AreaUnderRocChart, F1Chart, FalsePositiveRateChart, PrecisionChart, RecallChart,
  TruePositiveRateChart,
} from './charts';
import columns from './columns';

const { useGetReferenceModelQualityQuery } = modelsApiSlice;

function BinaryClassificationMetrics() {
  useGetCurrentModelQualityLatestQueryWithPolling();

  const { data, isLoading, isError } = useGetCurrentModelQuality();

  const jobStatus = data?.jobStatus;

  if (isError) {
    return <SomethingWentWrong />;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    const confusionMatrixLabel = {
      xAxisLabel: ['Predicted: 1', 'Predicted: 0'],
      yAxisLabel: ['Actual: 0', 'Actual: 1'],
    };

    const confusionMatrixData = [
      [data?.modelQuality.globalMetrics.truePositiveCount, data?.modelQuality.globalMetrics.falseNegativeCount],
      [data?.modelQuality.globalMetrics.falsePositiveCount, data?.modelQuality.globalMetrics.trueNegativeCount],
    ];

    return (
      <Spinner spinning={isLoading}>
        <div className="flex flex-col gap-4 p-4">
          <PerformanceBoard />

          <AccuracyChart />

          <PrecisionChart />

          <RecallChart />

          <F1Chart />

          <TruePositiveRateChart />

          <FalsePositiveRateChart />

          <ConfusionMatrix
            colors={[CHART_COLOR.WHITE, CHART_COLOR.CURRENT]}
            dataset={confusionMatrixData}
            labelClass={confusionMatrixLabel}
          />

          <AreaUnderRocChart />

          <AreaUnderPrChart />
        </div>
      </Spinner>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

function PerformanceBoard() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQuality();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceAccuracy = referenceData?.modelQuality?.accuracy;
  const referencePrecision = referenceData?.modelQuality?.precision;
  const referenceRecall = referenceData?.modelQuality?.recall;
  const referenceF1 = referenceData?.modelQuality?.f1;
  const referenceFalsePositiveRate = referenceData?.modelQuality?.falsePositiveRate;
  const referenceTruePositiveRate = referenceData?.modelQuality?.truePositiveRate;
  const referenceAreaUnderRoc = referenceData?.modelQuality?.areaUnderRoc;
  const referenceAreaUnderPr = referenceData?.modelQuality?.areaUnderPr;

  const leftTableData = currentData ? [
    {
      label: MODEL_QUALITY_FIELD.ACCURACY,
      referenceValue: referenceAccuracy,
      currentValue: currentData.modelQuality.globalMetrics.accuracy,
    },
    {
      label: MODEL_QUALITY_FIELD.PRECISION,
      referenceValue: referencePrecision,
      currentValue: currentData.modelQuality.globalMetrics.precision,
    },
    {
      label: MODEL_QUALITY_FIELD.RECALL,
      referenceValue: referenceRecall,
      currentValue: currentData.modelQuality.globalMetrics.recall,
    },
    {
      label: MODEL_QUALITY_FIELD.F1,
      referenceValue: referenceF1,
      currentValue: currentData.modelQuality.globalMetrics.f1,
    },
  ] : [];

  const centerTableData = currentData ? [
    {
      label: MODEL_QUALITY_FIELD.FALSE_POSITIVE_RATE,
      referenceValue: referenceFalsePositiveRate,
      currentValue: currentData.modelQuality.globalMetrics.falsePositiveRate,
    },
    {
      label: MODEL_QUALITY_FIELD.TRUE_POSITIVE_RATE,
      referenceValue: referenceTruePositiveRate,
      currentValue: currentData.modelQuality.globalMetrics.truePositiveRate,
    },
  ] : [];

  const rightTableData = currentData ? [
    {
      label: MODEL_QUALITY_FIELD.AREA_UNDER_ROC,
      referenceValue: referenceAreaUnderRoc,
      currentValue: currentData.modelQuality.globalMetrics.areaUnderRoc,
    },
    {
      label: MODEL_QUALITY_FIELD.AREA_UNDER_PR,
      referenceValue: referenceAreaUnderPr,
      currentValue: currentData.modelQuality.globalMetrics.areaUnderPr,
    },
  ] : [];

  return (
    <Board
      header={<SectionTitle size="small" title="Performance metrics" />}
      main={(
        <div className="flex flew-row gap-16">
          <DataTable
            columns={columns}
            dataSource={leftTableData}
            modifier="basis-1/3"
            pagination={false}
            rowKey={({ label }) => label}
            size="small"
          />

          <DataTable
            columns={columns}
            dataSource={centerTableData}
            modifier="basis-1/3"
            pagination={false}
            rowKey={({ label }) => label}
            size="small"
          />

          <DataTable
            columns={columns}
            dataSource={rightTableData}
            modifier="basis-1/3"
            pagination={false}
            rowKey={({ label }) => label}
            size="small"
          />
        </div>
      )}
      modifier="shadow"
      size="small"
      type="primary-light"
    />
  );
}

export default memo(BinaryClassificationMetrics);
