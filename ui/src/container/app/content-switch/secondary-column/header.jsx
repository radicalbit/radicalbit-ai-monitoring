import { PathsEnum } from '@Src/constants';

import SecondaryColumnModelsHeader from '@Src/container/models/Details/secondary-column/header';
import {
  Route,
  Routes,
} from 'react-router';

export default function SecondaryHeaderContentSwitch() {
  return (

    <Routes>
      <Route
        element={(<SecondaryColumnModelsHeader />)}
        path={`/${PathsEnum.MODELS_DETAIL}`}
      />

    </Routes>
  );
}
