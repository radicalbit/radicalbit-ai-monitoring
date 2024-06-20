import { ModelDetails } from './Details';
import { ModelsList } from './List';

export const modelsRoutes = {
  path: 'models',
  children: [
    { path: '', element: <ModelsList /> },
    { path: ':uuid', element: <ModelDetails /> },
  ],
};
