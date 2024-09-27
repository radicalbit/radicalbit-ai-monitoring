import { PathsEnum } from '@Src/constants';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { matchPath, useLocation } from 'react-router';
import { DETAIL_LAYOUT_CONFIGURATION, MAIN_LAYOUT_CONFIGURATION, NOT_FOUND_CONFIGURATION } from './layout-provider-configuration';

const allRoutes = [
  {
    key: `/${PathsEnum.LAUNCHPAD}`,
    layout: MAIN_LAYOUT_CONFIGURATION,
  },
  {
    key: `/${PathsEnum.MODELS}`,
    layout: MAIN_LAYOUT_CONFIGURATION,
  },
  {
    key: `/${PathsEnum.MODELS_DETAIL}`,
    layout: DETAIL_LAYOUT_CONFIGURATION,
  },
];

export function useLayoutProvider() {
  const { pathname } = useLocation();
  const dispatch = useDispatch();

  useEffect(() => {
    if (!allRoutes) {
      return;
    }

    // Get current route (exact: true)
    const layout = getCurrentRoute(allRoutes, pathname)?.layout ?? NOT_FOUND_CONFIGURATION;

    // Execute all the actions
    if (layout) {
      layout.forEach((action) => dispatch(action()));
    }
  }, [dispatch, pathname]);

  return null;
}

const getCurrentRoute = (routes, pathname) => routes.find(({ key: path }) => matchPath(path, pathname));

export { allRoutes };
