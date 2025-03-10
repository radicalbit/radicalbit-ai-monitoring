import DarkMode from '@Components/dark-mode';
import {
  DETAIL_LAYOUT_DARK_MODE_CONFIGURATION,
  DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import {
  NewHeader,
  RelativeDateTime,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router-dom';

const { useGetTracingProjectByUUIDQuery } = tracingApiSlice;

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
      }}
      title={<SectionTitle subtitle={<Subtitle />} title={<Title />} />}
    />
  );
}

function Title() {
  const { uuid } = useParams();
  const { data } = useGetTracingProjectByUUIDQuery({ uuid });

  const name = data?.name;

  return <h1>{name || ''}</h1>;
}

function Subtitle() {
  const { uuid } = useParams();
  const { data } = useGetTracingProjectByUUIDQuery({ uuid });

  const createdAt = data?.createdAt ?? 0;
  const updatedAt = data?.updatedAt ?? 0;

  return (
    <>
      {'Created: '}

      <RelativeDateTime threshold={3} timestamp={createdAt} withTooltip />

      {' • Updated: '}

      <RelativeDateTime threshold={3} timestamp={updatedAt} withTooltip />
    </>
  );
}

export default ProjectDetailHeader;
