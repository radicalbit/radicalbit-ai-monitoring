import { useIsDarkMode } from '@Components/dark-mode/hooks';
import { TRACING_TABS_ENUM } from '@Container/tracing/constants';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { selectors as layoutSelectors } from '@State/layout';
import { Menu, Truncate } from '@radicalbit/radicalbit-design-system';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import {
  useNavigate, useParams,
  useSearchParams,
} from 'react-router-dom';

const { selectHasSecondaryColumnCollapsed } = layoutSelectors;

const { useGetTracingProjectsQuery } = tracingApiSlice;

const commonChildrenMenu = () => {
  const commonMenu = [
    { label: 'Dashboard', key: TRACING_TABS_ENUM.DASHBOARD },
    { label: 'Traces', key: TRACING_TABS_ENUM.TRACES },
    { label: 'Sessions', key: TRACING_TABS_ENUM.SESSIONS },
    { label: 'Settings', key: TRACING_TABS_ENUM.SETTINGS },
  ];

  return commonMenu;
};

export default function ProjectDetailSecondaryColumnContent() {
  const { uuid } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const isDarkMode = useIsDarkMode();
  const theme = isDarkMode ? 'dark' : 'light';

  const isSecondaryColumnCollapsed = useSelector(selectHasSecondaryColumnCollapsed);

  const { data } = useGetTracingProjectsQuery();
  const items = data?.list ?? [];

  const menuItemList = items.map(({ uuid: tracingProjectUUID, name }) => ({
    label: (<Truncate>{name}</Truncate>),
    children: commonChildrenMenu(tracingProjectUUID),
    key: tracingProjectUUID,
    className: uuid === tracingProjectUUID ? Menu.HIDE_EXPAND_ICON : '',
  }));

  const [openKeys, setOpenKeys] = useState([uuid]);
  const rootSubmenuKeys = menuItemList.map(({ key }) => (key));

  const onOpenChange = (keys) => {
    const validKeys = (keys.length === 0) ? openKeys : keys;
    const latestOpenKey = validKeys.find((key) => openKeys.indexOf(key) === -1);
    if (!isSecondaryColumnCollapsed) {
      if (rootSubmenuKeys.indexOf(latestOpenKey) === -1) {
        setOpenKeys(validKeys);
      } else {
        setOpenKeys(latestOpenKey ? [latestOpenKey] : []);
      }
    }

    if (latestOpenKey !== undefined && uuid !== latestOpenKey) {
      navigate(`/projects/${latestOpenKey}?tab=${TRACING_TABS_ENUM.DASHBOARD}`);
    }
  };

  const handleOnTabsClick = (t) => {
    const tracingProjectUUID = t.keyPath[1];
    const modelTab = t.keyPath[0];

    navigate(`/projects/${tracingProjectUUID}?tab=${modelTab}`);
  };

  const selectedKeys = searchParams.get('tab') || TRACING_TABS_ENUM.DASHBOARD;

  return (
    <Menu
      items={menuItemList}
      mode="inline"
      onClick={handleOnTabsClick}
      onOpenChange={onOpenChange}
      openKeys={openKeys}
      selectedKeys={selectedKeys}
      theme={theme}
    />
  );
}
