import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
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
      details={{
        one: <AddNewModel />,
      }}
      title={<SectionTitle subtitle={<Subtitle />} title="Models" />}
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
    <Button onClick={onClick} shape="circle">
      <FontAwesomeIcon icon={faPlus} />
    </Button>
  );
}
