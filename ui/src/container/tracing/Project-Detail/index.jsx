import ComingSoonComponent from '@Components/coming-soon';
import { useInitDarkMode } from '@Components/dark-mode/hooks';
import {
  DETAIL_LAYOUT_DARK_MODE_CONFIGURATION,
  DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import { useSearchParams } from 'react-router-dom';
import { TRACING_TABS_ENUM } from '../constants';
import ProjectDashboard from './dashboard';
import SessionsList from './sessions';
import SessionsTracesList from './sessions/traces';
import TracesList from './traces';

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
  const [searchParams] = useSearchParams();
  const activeTab = searchParams.get('tab') || TRACING_TABS_ENUM.DASHBOARD;

  switch (activeTab) {
    case TRACING_TABS_ENUM.DASHBOARD:
      return <ProjectDashboard />;

    case TRACING_TABS_ENUM.TRACES:
      return <TracesList />;

    case TRACING_TABS_ENUM.SESSIONS:
      return <SessionsLayout />;

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
