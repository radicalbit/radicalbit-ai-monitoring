import JobStatusPin from '@Components/JobStatus/job-status-pin';
import { useIsDarkMode } from '@Components/dark-mode/hooks';
import { MODEL_TABS_ENUM } from '@Container/models/Details/constants';
import getJobStatus from '@Helpers/get-spinner-job-status';
import { selectors as layoutSelectors } from '@State/layout';
import { ModelTypeEnum } from '@State/models/constants';
import { useGetModelsQueryWithPolling } from '@State/models/polling-hook';
import { Menu, MenuInlineOnce, Truncate } from '@radicalbit/radicalbit-design-system';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';

const { selectHasSecondaryColumnCollapsed } = layoutSelectors;

const commonChildrenMenu = (modelType) => {
  switch (modelType) {
    case ModelTypeEnum.TEXT_GENERATION:
      return [{ label: 'Overview', key: MODEL_TABS_ENUM.OVERVIEW }];

    case ModelTypeEnum.EMBEDDINGS:
      return [
        { label: 'Reference', key: MODEL_TABS_ENUM.REFERENCE_DASHBOARD },
        { label: 'Current', key: MODEL_TABS_ENUM.CURRENT_DASHBOARD },
      ];

    default:
      return [
        { label: 'Overview', key: MODEL_TABS_ENUM.OVERVIEW },
        { label: 'Reference', key: MODEL_TABS_ENUM.REFERENCE_DASHBOARD },
        { label: 'Current', key: MODEL_TABS_ENUM.CURRENT_DASHBOARD },
      ];
  }
};

export default function SecondaryColumnModelsContent() {
  const isDarkMode = useIsDarkMode();
  const theme = isDarkMode ? 'dark' : 'light';

  const { uuid } = useParams();
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const submenuSelectedKey = searchParams.get('tab') || MODEL_TABS_ENUM.OVERVIEW;

  const [openKey, setOpenKey] = useState(uuid);

  const { data } = useGetModelsQueryWithPolling();
  const modelList = data?.items ?? [];

  const modelListMenuItem = modelList.map(({
    uuid: modelUUID, name, latestReferenceJobStatus, latestCurrentJobStatus, latestCompletionJobStatus, modelType,
  }) => {
    const jobStatus = getJobStatus({
      modelType,
      latestReferenceJobStatus,
      latestCurrentJobStatus,
      latestCompletionJobStatus,
    });

    const classNameHideIcon = uuid === modelUUID ? Menu.HIDE_EXPAND_ICON : '';

    return {
      label: <Label jobStatus={jobStatus} name={name} />,
      key: modelUUID,
      children: commonChildrenMenu(modelType),
      className: classNameHideIcon,
    };
  });

  const handleOnOpenChange = (keys) => {
    const nextOpenKey = keys.find((key) => openKey !== key);

    if (!nextOpenKey) {
      return;
    }

    setOpenKey(nextOpenKey);

    navigate({
      pathname: `/models/${nextOpenKey}`,
      search: searchParams.toString(),
    });
  };

  const handleOnTabsClick = ({ keyPath }) => {
    const modelTab = keyPath[0];
    const uuidFromKeyPath = (keyPath.length > 1) ? keyPath[1] : keyPath[0];
    navigate(`/models/${uuidFromKeyPath}?tab=${modelTab}`);
  };

  useAvoidGlitchWhileCollapsingColumn(setOpenKey);
  useAvoidGlitchWhileExpandingColumn(setOpenKey);

  return (
    <MenuInlineOnce
      items={modelListMenuItem}
      onClick={handleOnTabsClick}
      onOpenChange={handleOnOpenChange}
      openKey={openKey}
      selectedKey={submenuSelectedKey}
      theme={theme}
    />
  );
}

function Label({ jobStatus, name }) {
  return (
    <div className="flex gap-2 items-center">
      <JobStatusPin jobStatus={jobStatus} />

      <Truncate className="w-10/12">{name}</Truncate>
    </div>
  );
}

const useAvoidGlitchWhileCollapsingColumn = (setOpenKeys) => {
  const isSecondaryColumnCollapsed = useSelector(selectHasSecondaryColumnCollapsed);

  useEffect(() => {
    if (isSecondaryColumnCollapsed) {
      setOpenKeys();
    }
  }, [isSecondaryColumnCollapsed, setOpenKeys]);
};

const useAvoidGlitchWhileExpandingColumn = (setOpenKeys) => {
  const { uuid } = useParams();
  const isSecondaryColumnCollapsed = useSelector(selectHasSecondaryColumnCollapsed);

  useEffect(() => {
    if (!isSecondaryColumnCollapsed) {
      setTimeout(() => { setOpenKeys(uuid); });
    }

    return () => clearTimeout();
  }, [isSecondaryColumnCollapsed, setOpenKeys, uuid]);
};
