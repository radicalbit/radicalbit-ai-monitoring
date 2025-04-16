import DarkMode from '@Components/dark-mode';
import {
  DETAIL_LAYOUT_DARK_MODE_CONFIGURATION,
  DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import { tracingApiSlice } from '@State/tracing/api';
import {
  NewHeader,
  RelativeDateTime,
  SectionTitle,
  Skeleton,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router-dom';
import DropdownMenu from './dropdown-menu';

const { useGetProjectByUUIDQuery, useEditTracingProjectMutation } = tracingApiSlice;

function ProjectDetailHeader() {
  const isProjectTracingEnabled = getIsProjectTracingEnabled();

  if (isProjectTracingEnabled) {
    return <ProjectDetailHeaderInner />;
  }

  return false;
}

function ProjectDetailHeaderInner() {
  return (
    <NewHeader
      actions={{
        one: (
          <DarkMode
            darkActions={DETAIL_LAYOUT_DARK_MODE_CONFIGURATION}
            lightActions={DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION}
          />
        ),
        two: (<DropdownMenu />),
      }}
      title={<SectionTitle subtitle={<Subtitle />} title={<Title />} />}
    />
  );
}

function Title() {
  const { uuid } = useParams();
  const { data, isLoading } = useGetProjectByUUIDQuery({ uuid });
  const [, { isLoading: isEditing }] = useEditTracingProjectMutation({ fixedCacheKey: `edit-new-project-${uuid}` });

  const name = data?.name;

  if (isLoading || isEditing) {
    return <Skeleton.Input active />;
  }

  return <h1>{name || ''}</h1>;
}

function Subtitle() {
  const { uuid } = useParams();
  const { data, isSuccess } = useGetProjectByUUIDQuery({ uuid });

  const createdAt = data?.createdAt ?? 0;
  const updatedAt = data?.updatedAt ?? 0;

  if (isSuccess) {
    return (
      <>
        {'Created: '}

        <RelativeDateTime threshold={3} timestamp={createdAt} withTooltip />

        {' • Updated: '}

        <RelativeDateTime threshold={3} timestamp={updatedAt} withTooltip />
      </>
    );
  }

  return false;
}

export default ProjectDetailHeader;
