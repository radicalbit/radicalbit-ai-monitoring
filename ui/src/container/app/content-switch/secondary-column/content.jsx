import ProjectDetailSecondaryColumnContent from '@Container/tracing/project-detail/secondary-column/content';
import getIsProjectTracingEnabled from '@Hooks/feature-flag/get-is-project-tracing-enabled';
import { PathsEnum } from '@Src/constants';
import SecondaryColumnModelsContent from '@Src/container/models/Details/secondary-column/content';
import { Route, Routes } from 'react-router';

export default function SecondaryContentSwitch() {
  const isProjectTracingEnabled = getIsProjectTracingEnabled();

  return (
    <Routes>
      <Route
        element={<SecondaryColumnModelsContent />}
        path={`/${PathsEnum.MODELS_DETAIL}`}
      />

      {isProjectTracingEnabled && (
        <Route
          element={<ProjectDetailSecondaryColumnContent />}
          path={`/${PathsEnum.TRACING_PROJECT_DETAIL}`}
        />
      )}
    </Routes>
  );
}
