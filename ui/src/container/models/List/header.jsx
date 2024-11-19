import DarkMode from '@Components/dark-mode';
import { MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { modelsApiSlice } from '@State/models/api';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import {
  Button,
  FontAwesomeIcon,
  NewHeader,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';

const { useGetModelsQuery } = modelsApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

export default function MainListModelsHeader() {
  return (
    <NewHeader
      actions={{
        one: <DarkMode
          darkActions={MAIN_LAYOUT_DARK_MODE_CONFIGURATION}
          lightActions={MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION}
        />,
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
