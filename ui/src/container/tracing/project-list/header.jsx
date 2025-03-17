import DarkMode from '@Components/dark-mode';
import {
  MAIN_LAYOUT_DARK_MODE_CONFIGURATION,
  MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import useModals from '@Hooks/use-modals';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import {
  Button,
  FontAwesomeIcon,
  NewHeader,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';

const { useGetAllProjectQuery } = tracingApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

function ProjectListHeader() {
  const isProjectTracingEnabled = getIsProjectTracingEnabled();

  if (isProjectTracingEnabled) {
    return <ProjectListHeaderInner />;
  }

  return false;
}

function ProjectListHeaderInner() {
  return (
    <NewHeader
      actions={{
        one: (
          <DarkMode
            darkActions={MAIN_LAYOUT_DARK_MODE_CONFIGURATION}
            lightActions={MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION}
          />
        ),
        two: <AddNewProject />,
      }}
      title={(
        <>
          <h1>Projects</h1>

          <SectionTitle subtitle={<Subtitle />} />
        </>
      )}
    />
  );
}

function Subtitle() {
  const queryParams = useSelector((state) => selectQueryParamsSelector(state, NamespaceEnum.PROJECTS));
  const { data, isLoading, isError } = useGetAllProjectQuery({ queryParams });

  const count = data?.length;

  const label = count <= 1 ? 'project' : 'projects';

  if (isLoading) {
    return false;
  }

  if (isError) {
    return false;
  }

  return `${count} ${label}`;
}

function AddNewProject() {
  const { showModal } = useModals();

  const onClick = () => {
    showModal(ModalsEnum.ADD_NEW_PROJECT);
  };

  return (
    <Button onClick={onClick} shape="circle" title="New Model">
      <FontAwesomeIcon icon={faPlus} />
    </Button>
  );
}

export default ProjectListHeader;
