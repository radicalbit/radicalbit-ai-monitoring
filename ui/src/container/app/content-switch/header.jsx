import { PathsEnum } from '@Src/constants';
import MainModelsHeader from '@Src/container/models/Details/header';
import MainListModelsHeader from '@Src/container/models/List/header';
import LaunchpadHeader from '@Src/container/launchpad/header';
import { Navigate, Route, Routes } from 'react-router';
import ProjectListHeader from '@Container/tracing/project-list/header';
import ProjectDetailHeader from '@Container/tracing/project-detail/header/header';

export default function MainHeaderContentSwitch() {
  return (
    <Routes>

      <Route element={<LaunchpadHeader />} path={`/${PathsEnum.LAUNCHPAD}`} />

      <Route element={<MainListModelsHeader />} path={`/${PathsEnum.MODELS}`} />

      <Route element={<MainModelsHeader />} path={`/${PathsEnum.MODELS_DETAIL}`} />

      <Route element={<ProjectListHeader />} path={`/${PathsEnum.TRACING_PROJECT}`} />

      <Route element={<ProjectDetailHeader />} path={`/${PathsEnum.TRACING_PROJECT_DETAIL}`} />

      <Route element={<Navigate replace to={`/${PathsEnum.LAUNCHPAD}`} />} path="*" />
    </Routes>
  );
}
