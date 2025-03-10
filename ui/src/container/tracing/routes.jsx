import ProjectList from './project-list';
import ProjectDetail from './project-detail';

export const tracingRoutes = {
  path: 'projects',
  children: [
    { path: '', element: <ProjectList /> },
    { path: ':uuid', element: <ProjectDetail /> },
  ],
};
