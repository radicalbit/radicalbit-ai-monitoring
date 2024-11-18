import JobStatus from '@Components/JobStatus';
import { METRICS_TABS } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { useGetReferenceDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import RegressionDataQualityMetrics from './data-quality';
import Imports from './imports';
import RegressionModelQualityMetrics from './model-quality';
import RegressionDataDriftMetrics from './data-drift';

const tabs = [
  {
    label: METRICS_TABS.DATA_QUALITY,
    key: METRICS_TABS.DATA_QUALITY,
    children: <RegressionDataQualityMetrics />,
  },
  {
    label: METRICS_TABS.MODEL_QUALITY,
    key: METRICS_TABS.MODEL_QUALITY,
    children: <RegressionModelQualityMetrics />,
  },
  {
    label: METRICS_TABS.DATA_DRIFT,
    key: METRICS_TABS.DATA_DRIFT,
    children: <RegressionDataDriftMetrics />,
  },
  {
    label: METRICS_TABS.IMPORT,
    key: METRICS_TABS.IMPORT,
    children: <Imports />,
  },

];

export default function CurrentDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();

  const { data } = useGetReferenceDataQualityQueryWithPolling();
  const jobStatus = data?.jobStatus;

  const activeTab = searchParams.get('tab-metrics') || METRICS_TABS.METRICS;

  const onChangeTab = (value) => {
    searchParams.set('tab-metrics', value);
    setSearchParams(searchParams);
  };

  if (jobStatus !== JOB_STATUS.SUCCEEDED) {
    return <JobStatus jobStatus={jobStatus} />;
  }

  return (
    <div className="h-full">
      <Tabs
        activeKey={activeTab}
        fullHeight
        items={tabs}
        noBorder
        onChange={onChangeTab}
      />
    </div>
  );
}
