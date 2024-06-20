import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import { METRICS_TABS } from '@Container/models/Details/constants';
import DataDriftMetrics from '../../data-drift-metrics';
import DataQualityMetrics from '../../data-quality-metrics';
import ModelQualityMetrics from '../../model-quality-metrics';

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
];

export default function CurrentDashboardModal() {
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('modal-tab-metrics') || METRICS_TABS.METRICS;

  const setTab = (value) => {
    searchParams.set('modal-tab-metrics', value);
    setSearchParams(searchParams);
  };

  const onChangeTab = (e) => {
    setTab(e);
  };

  return (

    <div className="px-4 pt-4 h-[99%]">
      <Tabs
        activeKey={activeTab}
        fullHeight
        items={tabs}
        onChange={onChangeTab}
      />
    </div>
  );
}
