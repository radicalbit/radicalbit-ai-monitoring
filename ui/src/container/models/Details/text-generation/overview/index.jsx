import JobStatus from '@Components/JobStatus';
import { METRICS_TABS } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { useGetCompletionModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import Imports from './imports';
import ModelQualityMetrics from './model-quality';

const tabs = [
  {
    label: METRICS_TABS.MODEL_QUALITY,
    key: METRICS_TABS.MODEL_QUALITY,
    children: <ModelQualityMetrics />,
  },
  {
    label: METRICS_TABS.IMPORT,
    key: METRICS_TABS.IMPORT,
    children: <Imports />,
  },

];

export default function OverviewDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();

  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const jobStatus = data?.jobStatus;

  const activeTab = searchParams.get('tab-metrics') || METRICS_TABS.MODEL_QUALITY;

  const setTab = (value) => {
    searchParams.set('tab-metrics', value);
    setSearchParams(searchParams);
  };

  const onChangeTab = (e) => {
    setTab(e);
  };

  if (!data) {
    return <JobStatus jobStatus={JOB_STATUS.MISSING_COMPLETION} />;
  }

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
