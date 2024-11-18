import {
  Tabs,
} from '@radicalbit/radicalbit-design-system';
import { useSearchParams } from 'react-router-dom';
import { MODEL_TABS_ENUM, OVERVIEW_TABS_ENUM } from '@Container/models/Details/constants';
import OutputsTab from './outputs-tab';
import SummaryTab from './summary-tab';
import VariablesTab from './variables-tab';

function Overview() {
  const [searchParams, setSearchParams] = useSearchParams();

  const activeKey = useGetTabParam();

  const handleOnChange = (key) => {
    searchParams.set(MODEL_TABS_ENUM.OVERVIEW, key);
    setSearchParams(searchParams);
  };

  const tabs = [
    {
      label: 'Summary',
      key: OVERVIEW_TABS_ENUM.SUMMARY,
      children: <SummaryTab />,

    },
    {
      label: 'Variables',
      key: OVERVIEW_TABS_ENUM.VARIABLES,
      children: <VariablesTab />,
    },
    {
      label: 'Outputs',
      key: OVERVIEW_TABS_ENUM.OUTPUTS,
      children: <OutputsTab />,
    },
  ];

  return (
    <Tabs
      activeKey={activeKey}
      animated={false}
      fullHeight
      items={tabs}
      noBorder
      onChange={handleOnChange}
    />
  );
}

const useGetTabParam = () => {
  const [searchParams] = useSearchParams();

  const tab = searchParams.get(MODEL_TABS_ENUM.OVERVIEW);

  return tab ? OVERVIEW_TABS_ENUM[tab.toUpperCase()] : OVERVIEW_TABS_ENUM.SUMMARY;
};

export default Overview;
