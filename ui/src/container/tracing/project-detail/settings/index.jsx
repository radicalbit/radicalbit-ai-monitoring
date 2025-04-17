import InstructionsComponent from '@Container/tracing/project-detail/void-instructions';
import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import ApiKeysProject from './api-keys';
import { SETTINGS_TABS } from './constants';

function Settings() {
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('tab-settings') || SETTINGS_TABS.HOW_TO_CONNECT;

  const handleOnChangeTab = (value) => {
    searchParams.set('tab-settings', value);
    setSearchParams(searchParams);
  };

  return (
    <Tabs
      activeKey={activeTab}
      fullHeight
      items={tabs}
      onChange={handleOnChangeTab}
    />
  );
}

const tabs = [
  {
    label: SETTINGS_TABS.HOW_TO_CONNECT,
    key: SETTINGS_TABS.HOW_TO_CONNECT,
    children: (
      <div className="max-w-[800px] w-full justify-self-center m-8">
        <InstructionsComponent />
      </div>),
  },
  {
    label: SETTINGS_TABS.API_KEYS,
    key: SETTINGS_TABS.API_KEYS,
    children: (
      <div className="max-w-[800px] w-full justify-self-center m-8">
        <ApiKeysProject />
      </div>),
  },
];

export default Settings;
