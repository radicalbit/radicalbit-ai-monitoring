import { NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { modelsApiSlice } from '@State/models/api';
import { SectionTitle } from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const { useGetModelsQuery } = modelsApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

export default function SecondaryColumnModelsHeader() {
  const navigate = useNavigate();

  const handleOnClick = () => {
    navigate('/models');
  };

  return (
    <SectionTitle
      onClick={handleOnClick}
      subtitle={<Subtitle />}
      title="Models"
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
