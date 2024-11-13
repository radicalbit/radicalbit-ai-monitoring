import {
  MAIN_LAYOUT_DARK_MODE_CONFIGURATION,
  MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { modelsApiSlice } from '@State/models/api';
import { faMoon, faPlus, faSun } from '@fortawesome/free-solid-svg-icons';
import {
  Button,
  FontAwesomeIcon,
  NewHeader,
  SectionTitle,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

const { useGetModelsQuery } = modelsApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

export default function MainListModelsHeader() {
  return (
    <NewHeader
      actions={{
        one: <DarkMode />,
        two: <AddNewModel />,
      }}
      title={(
        <>
          <h1>Models</h1>

          <SectionTitle subtitle={<Subtitle />} />
        </>
      )}
    />
  );
}

function Subtitle() {
  const queryParams = useSelector((state) => selectQueryParamsSelector(state, NamespaceEnum.MODELS));
  const { data, isLoading, isError } = useGetModelsQuery({ queryParams });

  const count = data?.total;

  const label = count <= 1 ? 'Model' : 'Models';

  if (isLoading) {
    return false;
  }

  if (isError) {
    return false;
  }

  return `${count} ${label}`;
}

function AddNewModel() {
  const { showModal } = useModals();

  const onClick = () => {
    showModal(ModalsEnum.ADD_NEW_MODEL);
  };

  return (
    <Button onClick={onClick} shape="circle" title="New Model">
      <FontAwesomeIcon icon={faPlus} />
    </Button>
  );
}

function DarkMode() {
  const dispatch = useDispatch();
  const [isDarkMode, setIsDarkMode] = useState(!!window.localStorage.getItem('enable-dark-mode'));

  const handleOnEnableDarkMode = () => {
    window.localStorage.setItem('enable-dark-mode', true);
    setIsDarkMode(true);

    MAIN_LAYOUT_DARK_MODE_CONFIGURATION.forEach((action) => dispatch(action()));
  };

  const handleOnEnableLightMode = () => {
    window.localStorage.removeItem('enable-dark-mode');
    setIsDarkMode(false);

    MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION.forEach((action) => dispatch(action()));
  };

  if (isDarkMode) {
    return (
      <Tooltip title="Switch to light mode">
        <FontAwesomeIcon icon={faMoon} onClick={handleOnEnableLightMode} />
      </Tooltip>
    );
  }

  return (
    <Tooltip title="Switch to dark mode">
      <FontAwesomeIcon icon={faSun} onClick={handleOnEnableDarkMode} />
    </Tooltip>
  );
}
