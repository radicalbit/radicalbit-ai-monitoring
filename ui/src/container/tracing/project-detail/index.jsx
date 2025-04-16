import ComingSoonComponent from '@Components/coming-soon';
import { useInitDarkMode } from '@Components/dark-mode/hooks';
import {
  DETAIL_LAYOUT_DARK_MODE_CONFIGURATION,
  DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import { tracingApiSlice } from '@State/tracing/api';
import { useParams, useSearchParams } from 'react-router-dom';
import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { TRACING_TABS_ENUM } from '../constants';
import ProjectDashboard from './dashboard';
import SessionsList from './sessions';
import SessionsTracesList from './sessions/traces';
import Settings from './settings';
import TracesList from './traces';

const { useGetProjectByUUIDQuery } = tracingApiSlice;

function ProjectDetail() {
  const isProjectTracingEnabled = getIsProjectTracingEnabled();

  useInitDarkMode(
    DETAIL_LAYOUT_DARK_MODE_CONFIGURATION,
    DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION,
  );

  if (isProjectTracingEnabled) {
    return <ProjectDetailInner />;
  }

  return <ComingSoonComponent />;
}

function ProjectDetailInner() {
  const { uuid } = useParams();

  const [searchParams] = useSearchParams();
  const activeTab = searchParams.get('tab') || TRACING_TABS_ENUM.DASHBOARD;

  const { isError } = useGetProjectByUUIDQuery({ uuid });

  if (isError) {
    return <SomethingWentWrong />;
  }

  switch (activeTab) {
    case TRACING_TABS_ENUM.DASHBOARD:
      return <ProjectDashboard />;

    case TRACING_TABS_ENUM.TRACES:
      return <TracesList />;

    case TRACING_TABS_ENUM.SESSIONS:
      return <SessionsLayout />;

    case TRACING_TABS_ENUM.SETTINGS:
      return <Settings />;

    default:
      return false;
  }
}

function SessionsLayout() {
  const [searchParams] = useSearchParams();
  const sessionUUID = searchParams.get('sessionUuid');

  if (sessionUUID === null) {
    return <SessionsList />;
  }

  return <SessionsTracesList />;
}

export default ProjectDetail;
