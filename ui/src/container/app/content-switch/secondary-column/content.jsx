import { PathsEnum } from '@Src/constants';
import SecondaryColumnModelsContent from '@Src/container/models/Details/secondary-column/content';
import { Route, Routes } from 'react-router';

export default function SecondaryContentSwitch() {
  return (
    <Routes>
      <Route
        element={(<SecondaryColumnModelsContent />)}
        path={`/${PathsEnum.MODELS_DETAIL}`}
      />
    </Routes>
  );
}
