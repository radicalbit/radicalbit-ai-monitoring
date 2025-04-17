import { METRICS_TABS } from '@Container/models/Details/constants';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import Imports from './imports';
import EmbeddingsCurrentDrift from './drift';

const tabs = [
  {
    label: METRICS_TABS.DATA_DRIFT,
    key: METRICS_TABS.DATA_DRIFT,
    children: <EmbeddingsCurrentDrift />,
  },
  {
    label: METRICS_TABS.IMPORT,
    key: METRICS_TABS.IMPORT,
    children: <Imports />,
  },

];

export default function CurrentDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('tab-metrics') || METRICS_TABS.DATA_DRIFT;

  const onChangeTab = (value) => {
    searchParams.set('tab-metrics', value);
    setSearchParams(searchParams);
  };

  return (
    <Tabs
      activeKey={activeTab}
      fullHeight
      items={tabs}
      noBorder
      onChange={onChangeTab}
    />
  );
}
