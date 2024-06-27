import JobStatus from '@Components/JobStatus';
import { METRICS_TABS } from '@Container/models/Details/constants';
import { JOB_STATUS } from '@Src/constants';
import { useGetReferenceDataQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import DataDriftMetrics from './data-drift/binary-classification';
import DataQualityMetrics from './data-quality';
import Imports from './imports';
import ModelQualityMetrics from './model-quality';

const tabs = [
  {
    label: METRICS_TABS.DATA_QUALITIY,
    key: METRICS_TABS.DATA_QUALITIY,
    children: <DataQualityMetrics />,
  },
  {
    label: METRICS_TABS.MODEL_QUALITY,
    key: METRICS_TABS.MODEL_QUALITY,
    children: <ModelQualityMetrics />,
  },
  {
    label: METRICS_TABS.DATA_DRIFT,
    key: METRICS_TABS.DATA_DRIFT,
    children: <DataDriftMetrics />,
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
        onChange={onChangeTab}
      />
    </div>
  );
}
