import Launchpad from '.';

export const launchpadRoutes = {
  path: '/',
  children: [
    { path: '', element: <Launchpad /> },
  ],
};
