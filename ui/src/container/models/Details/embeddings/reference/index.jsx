import { METRICS_TABS } from '@Container/models/Details/constants';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import EmbeddingsReferenceDrift from './drift';
import Imports from './imports';

const tabs = [
  {
    label: METRICS_TABS.DATA_DRIFT,
    key: METRICS_TABS.DATA_DRIFT,
    children: <EmbeddingsReferenceDrift />,
  },
  {
    label: METRICS_TABS.IMPORT,
    key: METRICS_TABS.IMPORT,
    children: <Imports />,
  },

];

export default function ReferenceDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('tab-metrics') || METRICS_TABS.DATA_DRIFT;

  const setTab = (value) => {
    searchParams.set('tab-metrics', value);
    setSearchParams(searchParams);
  };

  const onChangeTab = (e) => {
    setTab(e);
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
