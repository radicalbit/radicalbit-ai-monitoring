import { NamespaceEnum } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { SectionTitle, Skeleton } from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const { useGetAllProjectQuery } = tracingApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

function ProjectDetailSecondaryColumnHeader() {
  const navigate = useNavigate();

  const handleOnClick = () => {
    navigate('/projects');
  };

  return (
    <SectionTitle
      onClick={handleOnClick}
      subtitle={<Subtitle />}
      title="Projects"
    />
  );
}

function Subtitle() {
  const queryParams = useSelector((state) => selectQueryParamsSelector(state, NamespaceEnum.PROJECTS));

  const { data, isLoading, isError } = useGetAllProjectQuery({ queryParams });

  const count = data?.length;

  const label = count <= 1 ? 'Project' : 'Projects';

  if (isLoading) {
    return <Skeleton.Input active size="small" />;
  }

  if (isError) {
    return false;
  }

  return `${count} ${label}`;
}

export default ProjectDetailSecondaryColumnHeader;
