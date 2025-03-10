import ComingSoonComponent from '@Components/coming-soon';
import { useInitDarkMode } from '@Components/dark-mode/hooks';
import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import SmartTable from '@Components/smart-table';
import {
  MAIN_LAYOUT_DARK_MODE_CONFIGURATION,
  MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import LogoSquared from '@Img/logo-collapsed.svg';
import { Spinner, Void } from '@radicalbit/radicalbit-design-system';
import { NamespaceEnum } from '@Src/constants';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useLocation, useNavigate } from 'react-router';
import { getColumns } from './columns';

const { useGetTracingProjectsQuery } = tracingApiSlice;

function ProjectList() {
  const isProjectTracingEnabled = getIsProjectTracingEnabled();

  useInitDarkMode(
    MAIN_LAYOUT_DARK_MODE_CONFIGURATION,
    MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION,
  );

  if (isProjectTracingEnabled) {
    return <ProjectListInner />;
  }

  return <ComingSoonComponent />;
}

function ProjectListInner() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const { data, isLoading, isError } = useGetTracingProjectsQuery();

  const projectList = data?.list ?? [];
  const count = data?.total || 0;

  const modifier = projectList?.length ? '' : 'c-spinner--centered';

  if (isError) {
    return <SomethingWentWrong />;
  }

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
      {!projectList.length && (
        <Void
          image={<LogoSquared />}
          title="Show a basic info to enable tracing"
        />
      )}

      {!!projectList.length && (
        <SmartTable
          clickable
          columns={getColumns}
          dataSource={projectList}
          namespace={NamespaceEnum.PROJECTS}
          onRow={({ uuid }) => ({
            onClick: () => navigate({
              pathname: `${uuid}`,
              search,
            }),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ uuid }) => uuid}
        />
      )}
    </Spinner>
  );
}

export default ProjectList;
