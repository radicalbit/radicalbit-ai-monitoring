import ProjectDetailSecondaryColumnHeader from '@Container/tracing/project-detail/secondary-column/header';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import { PathsEnum } from '@Src/constants';
import SecondaryColumnModelsHeader from '@Src/container/models/Details/secondary-column/header';
import { Route, Routes } from 'react-router';

export default function SecondaryHeaderContentSwitch() {
  const isProjectTracingEnabled = getIsProjectTracingEnabled();

  return (
    <Routes>
      <Route
        element={<SecondaryColumnModelsHeader />}
        path={`/${PathsEnum.MODELS_DETAIL}`}
      />

      {isProjectTracingEnabled && (
        <Route
          element={<ProjectDetailSecondaryColumnHeader />}
          path={`/${PathsEnum.TRACING_PROJECT_DETAIL}`}
        />
      )}
    </Routes>
  );
}
