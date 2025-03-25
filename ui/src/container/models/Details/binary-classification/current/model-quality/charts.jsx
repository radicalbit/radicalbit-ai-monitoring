import { CHART_COLOR } from '@Helpers/common-chart-options';
import LineChart from '@Components/charts/line-chart';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { useGetCurrentModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { modelsApiSlice } from '@State/models/api';
import { useParams } from 'react-router-dom';

const { useGetReferenceModelQualityQuery } = modelsApiSlice;

function AccuracyChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceAccuracy = referenceData?.modelQuality?.accuracy;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.accuracy;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceAccuracy }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.ACCURACY}
      />
    );
  }

  return false;
}

function PrecisionChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referencePrecision = referenceData?.modelQuality?.precision;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.precision;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referencePrecision }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.PRECISION}
      />
    );
  }
  return false;
}

function RecallChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceRecall = referenceData?.modelQuality?.recall;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.recall;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceRecall }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.RECALL}
      />
    );
  }
  return false;
}

function F1Chart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceF1 = referenceData?.modelQuality?.f1;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.f1;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceF1 }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.F1}
      />
    );
  }
  return false;
}

function FalsePositiveRateChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceFalsePositiveRate = referenceData?.modelQuality?.falsePositiveRate;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.falsePositiveRate;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceFalsePositiveRate }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.FALSE_POSITIVE_RATE}
      />
    );
  }

  return false;
}

function TruePositiveRateChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceTruePositiveRate = referenceData?.modelQuality?.truePositiveRate;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.truePositiveRate;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceTruePositiveRate }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.TRUE_POSITIVE_RATE}
      />
    );
  }

  return false;
}

function AreaUnderRocChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceAreaUnderRoc = referenceData?.modelQuality?.areaUnderRoc;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.areaUnderRoc;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceAreaUnderRoc }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.AREA_UNDER_ROC}
      />
    );
  }
  return false;
}
function AreaUnderPrChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceAreaUnderPr = referenceData?.modelQuality?.areaUnderPr;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.areaUnderPr;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceAreaUnderPr }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.AREA_UNDER_PR}
      />
    );
  }
  return false;
}

function LogLossChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceAreaUnderPr = referenceData?.modelQuality?.logLoss;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.logLoss;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceAreaUnderPr }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.LOG_LOSS}
      />
    );
  }
  return false;
}

export {
  AccuracyChart, AreaUnderPrChart, AreaUnderRocChart, F1Chart,
  FalsePositiveRateChart, PrecisionChart,
  RecallChart, TruePositiveRateChart, LogLossChart,
};
