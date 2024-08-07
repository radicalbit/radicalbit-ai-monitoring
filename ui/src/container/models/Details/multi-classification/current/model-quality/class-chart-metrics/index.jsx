import { MODEL_QUALITY_FIELD } from '@Container/models/Details/constants';
import useGetDataCharts from '../use-get-data-charts';
import LineChart from './chart';

function MulticlassChartMetrics() {
  return (
    <div className="flex flex-col gap-4">
      <RecallChart />

      <F1MeasureChart />

      <PrecisionChart />

      <FalsePositiveRateChart />

      <TruePositiveRateChart />
    </div>
  );
}

function RecallChart() {
  const items = useGetDataCharts();

  const currentSeries = items.map(({ className, currentData }) => ({ className, data: currentData.recall }));
  const referenceSeries = items.map(({ className, referenceData, currentData }) => ({
    className,
    data: currentData.recall.map((o) => ({
      timestamp: o.timestamp,
      value: referenceData.recall,
    })),
  }));

  return (
    <LineChart
      currentData={currentSeries}
      referenceData={referenceSeries}
      title={MODEL_QUALITY_FIELD.RECALL}
    />
  );
}

function F1MeasureChart() {
  const items = useGetDataCharts();

  const currentSeries = items.map(({ className, currentData }) => ({ className, data: currentData.fMeasure }));
  const referenceSeries = items.map(({ className, referenceData, currentData }) => ({
    className,
    data: currentData.fMeasure.map((o) => ({
      timestamp: o.timestamp,
      value: referenceData.fMeasure,
    })),
  }));

  return (
    <LineChart
      currentData={currentSeries}
      referenceData={referenceSeries}
      title={MODEL_QUALITY_FIELD.F1}
    />
  );
}

function PrecisionChart() {
  const items = useGetDataCharts();

  const currentSeries = items.map(({ className, currentData }) => ({ className, data: currentData.precision }));
  const referenceSeries = items.map(({ className, referenceData, currentData }) => ({
    className,
    data: currentData.precision.map((o) => ({
      timestamp: o.timestamp,
      value: referenceData.precision,
    })),
  }));

  return (
    <LineChart
      currentData={currentSeries}
      referenceData={referenceSeries}
      title={MODEL_QUALITY_FIELD.PRECISION}
    />
  );
}

function FalsePositiveRateChart() {
  const items = useGetDataCharts();

  const currentSeries = items.map(({ className, currentData }) => ({ className, data: currentData.falsePositiveRate }));
  const referenceSeries = items.map(({ className, referenceData, currentData }) => ({
    className,
    data: currentData.falsePositiveRate.map((o) => ({
      timestamp: o.timestamp,
      value: referenceData.falsePositiveRate,
    })),
  }));

  return (
    <LineChart
      currentData={currentSeries}
      referenceData={referenceSeries}
      title={MODEL_QUALITY_FIELD.FALSE_POSITIVE_RATE}
    />
  );
}

function TruePositiveRateChart() {
  const items = useGetDataCharts();

  const currentSeries = items.map(({ className, currentData }) => ({ className, data: currentData.truePositiveRate }));

  const referenceSeries = items.map(({ className, referenceData, currentData }) => ({
    className,
    data: currentData.truePositiveRate.map((o) => ({
      timestamp: o.timestamp,
      value: referenceData.truePositiveRate,
    })),
  }));

  return (
    <LineChart
      currentData={currentSeries}
      referenceData={referenceSeries}
      title={MODEL_QUALITY_FIELD.TRUE_POSITIVE_RATE}
    />
  );
}

export default MulticlassChartMetrics;
