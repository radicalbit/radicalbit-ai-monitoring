import { modelsApiSlice } from '@Src/store/state/models/api';
import { Menu } from '@radicalbit/radicalbit-design-system';
import { useEffect, useState } from 'react';
import {
  useNavigate, useParams, useSearchParams,
} from 'react-router-dom';
import { selectors as layoutSelectors } from '@State/layout';
import { useSelector } from 'react-redux';
import JobStatusPin from '@Components/JobStatus/job-status-pin';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { NamespaceEnum } from '@Src/constants';
import { MODEL_TABS_ENUM } from '../constants';

const { useGetModelsQuery } = modelsApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

const commonChildrenMenu = [
  { label: 'Overview', key: MODEL_TABS_ENUM.OVERVIEW },
  { label: 'Reference', key: MODEL_TABS_ENUM.REFERENCE_DASHBOARD },
  { label: 'Current', key: MODEL_TABS_ENUM.CURRENT_DASHBOARD },
];

const { selectHasSecondaryColumnCollapsed } = layoutSelectors;

export default function SecondaryColumnModelsContent() {
  const { uuid } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const isSecondaryColumnCollapsed = useSelector(selectHasSecondaryColumnCollapsed);

  const queryParams = useSelector((state) => selectQueryParamsSelector(state, NamespaceEnum.MODELS));

  const { data } = useGetModelsQuery({ queryParams });
  const modelList = data?.items ?? [];
  const modelListMenuItem = modelList.map(({ uuid: modelUUID, name }) => (
    {
      label: (
        <div className="flex gap-2 items-center">
          <div>{name}</div>

          <JobStatusPin uuid={modelUUID} />
        </div>),
      key: modelUUID,
      children: commonChildrenMenu,
      className: uuid === modelUUID ? Menu.HIDE_EXPAND_ICON : '',
    }
  ));

  const [openKeys, setOpenKeys] = useState([uuid]);
  const rootSubmenuKeys = modelListMenuItem.map(({ key }) => (key));

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
      navigate(`/models/${latestOpenKey}?tab=${MODEL_TABS_ENUM.OVERVIEW}`);
    }
  };

  const selectedKeys = searchParams.get('tab') || MODEL_TABS_ENUM.OVERVIEW;

  const handleOnTabsClick = (t) => {
    const modelUUID = t.keyPath[1];
    const modelTab = t.keyPath[0];
    navigate(`/models/${modelUUID}?tab=${modelTab}`);
  };

  useAvoidGlitchWhileCollapsingColumn(setOpenKeys);
  useAvoidGlitchWhileExpandingColumn(setOpenKeys);

  return (
    <Menu
      items={modelListMenuItem}
      mode="inline"
      onClick={handleOnTabsClick}
      onOpenChange={onOpenChange}
      openKeys={openKeys}
      selectedKeys={selectedKeys}
      theme="dark"
    />
  );
}

const useAvoidGlitchWhileCollapsingColumn = (setOpenKeys) => {
  const isSecondaryColumnCollapsed = useSelector(selectHasSecondaryColumnCollapsed);

  useEffect(() => {
    if (isSecondaryColumnCollapsed) {
      setOpenKeys([]);
    }
  }, [isSecondaryColumnCollapsed, setOpenKeys]);
};

const useAvoidGlitchWhileExpandingColumn = (setOpenKeys) => {
  const { uuid } = useParams();
  const isSecondaryColumnCollapsed = useSelector(selectHasSecondaryColumnCollapsed);

  useEffect(() => {
    if (!isSecondaryColumnCollapsed) {
      setTimeout(() => { setOpenKeys([uuid]); });
    }

    return () => clearTimeout();
  }, [isSecondaryColumnCollapsed, setOpenKeys, uuid]);
};
