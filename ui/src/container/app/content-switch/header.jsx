import { PathsEnum } from '@Src/constants';
import MainModelsHeader from '@Src/container/models/Details/header';
import MainListModelsHeader from '@Src/container/models/List/header';
import LaunchpadHeader from '@Src/container/launchpad/header';
import { Navigate, Route, Routes } from 'react-router';

export default function MainHeaderContentSwitch() {
  return (
    <Routes>

      <Route element={<LaunchpadHeader />} path="/" />

      <Route element={<MainListModelsHeader />} path={`/${PathsEnum.MODELS}`} />

      <Route element={<MainModelsHeader />} path={`/${PathsEnum.MODELS_DETAIL}`} />

      <Route element={<Navigate replace to="/" />} path="*" />
    </Routes>
  );
}
