import { CHART_COLOR } from '@Helpers/common-chart-options';
import LineChart from '@Components/charts/line-chart';
import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import { useGetCurrentModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { modelsApiSlice } from '@State/models/api';
import { useParams } from 'react-router';

const { useGetReferenceModelQualityQuery } = modelsApiSlice;

function MseChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceMse = referenceData?.modelQuality?.mse;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.mse;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceMse }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.MSE}
      />
    );
  }

  return false;
}

function RmseChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceRmse = referenceData?.modelQuality?.rmse;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.rmse;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceRmse }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.RMSE}
      />
    );
  }

  return false;
}

function MaeChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceMae = referenceData?.modelQuality?.mae;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.mae;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceMae }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.MAE}
      />
    );
  }

  return false;
}

function MapeChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceMape = referenceData?.modelQuality?.mape;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.mape;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceMape }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.MAPE}
      />
    );
  }

  return false;
}

function R2Chart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceR2 = referenceData?.modelQuality?.r2;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.r2;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceR2 }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.R2}
      />
    );
  }

  return false;
}

function AdjR2Chart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceAdjR2 = referenceData?.modelQuality?.adjR2;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.adjR2;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceAdjR2 }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.ADJ_R2}
      />
    );
  }

  return false;
}

function VarianceChart() {
  const { uuid } = useParams();
  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQuery({ uuid });

  const referenceVariance = referenceData?.modelQuality?.variance;
  const currentSeries = currentData?.modelQuality?.groupedMetrics?.variance;

  if (currentSeries && currentSeries !== null) {
    const referenceSeries = currentSeries.map((o) => ({ ...o, value: referenceVariance }));

    return (
      <LineChart
        color={CHART_COLOR.CURRENT}
        currentData={currentSeries}
        referenceData={referenceSeries}
        title={MODEL_QUALITY_FIELD.VARIANCE}
      />
    );
  }

  return false;
}

export {
  MseChart,
  RmseChart,
  MaeChart,
  MapeChart,
  R2Chart,
  AdjR2Chart,
  VarianceChart,
};
