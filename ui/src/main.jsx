import { initializeFaro, withFaroRouterInstrumentation } from '@grafana/faro-react';
import React, { StrictMode, Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { getCookieConsentValue } from 'react-cookie-consent';
import { v4 as uuidv4 } from 'uuid';
import { launchpadRoutes } from '@Container/launchpad/routes';
import { notFoundRoute } from './components/ErrorPage';
import App from './container/app';
import { modelsRoutes } from './container/models/routes';
import { store } from './store/configureStore';

const getGrafanaTracking = (enableGrafanaTracking) => {
  let tracking;

  if (enableGrafanaTracking === 'true') {
    if (tracking === undefined) {
      const userUUID = localStorage.getItem('radicalbit_user_uuid') === null ? uuidv4() : localStorage.getItem('radicalbit_user_uuid');
      localStorage.setItem('radicalbit_user_uuid', userUUID);

      tracking = initializeFaro({
        url: 'https://telemetry.oss.radicalbit.ai',
        apiKey: 'rbitoss-JpIYMVC677edETUbJN9Me3iLS7ngGaE2RYLzQWCOYVljUJh5JJk5o2FE',
        app: { name: 'radicalbit-ai-monitoring' },
        sessionTracking: { enabled: true },
      });
      tracking.api.setSession({ id: userUUID });
    }
  }
  return tracking;
};

const enableGrafanaTracking = getCookieConsentValue('rbit-tracking');
export const grafanaTracking = getGrafanaTracking(enableGrafanaTracking);

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      launchpadRoutes,
      modelsRoutes,
      notFoundRoute,
    ],
  },
]);

const browserRouter = (enableGrafanaTracking === 'true') ? withFaroRouterInstrumentation(router) : router;

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <Suspense fallback={<div />}>
        <StrictMode>
          <RouterProvider router={browserRouter} />
        </StrictMode>
      </Suspense>
    </Provider>
  </React.StrictMode>,
);
