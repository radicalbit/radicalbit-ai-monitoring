import JobStatus from '@Components/JobStatus';
import { METRICS_TABS } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { useGetReferenceDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import BinaryClassificationDataQualityMetrics from './data-quality';
import Imports from './imports';
import BinaryClassificationModelQualityMetrics from './model-quality';
import BinaryClassificationDataDriftMetrics from './data-drift';

const tabs = [
  {
    label: METRICS_TABS.DATA_QUALITY,
    key: METRICS_TABS.DATA_QUALITY,
    children: <BinaryClassificationDataQualityMetrics />,
  },
  {
    label: METRICS_TABS.MODEL_QUALITY,
    key: METRICS_TABS.MODEL_QUALITY,
    children: <BinaryClassificationModelQualityMetrics />,
  },
  {
    label: METRICS_TABS.DATA_DRIFT,
    key: METRICS_TABS.DATA_DRIFT,
    children: <BinaryClassificationDataDriftMetrics />,
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
    <div className="px-4 pt-4 h-full">
      <Tabs
        activeKey={activeTab}
        fullHeight
        items={tabs}
        onChange={onChangeTab}
      />
    </div>
  );
}
