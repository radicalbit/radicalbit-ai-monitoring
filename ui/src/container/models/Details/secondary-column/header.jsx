import { NamespaceEnum } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { SectionTitle } from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

const { useGetModelsQuery } = modelsApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

export default function SecondaryColumnModelsHeader() {
  return (
    <Link to="/models">
      <SectionTitle
        subtitle={<Subtitle />}
        title="Models"
      />
    </Link>
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
