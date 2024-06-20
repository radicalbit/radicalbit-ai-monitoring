import NotFound from './not-found';

export const notFoundRoute = {
  path: '/*',
  children: [{ path: '*', element: <NotFound /> }],
};
