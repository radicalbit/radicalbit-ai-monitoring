import { initializeFaro, withFaroRouterInstrumentation } from '@grafana/faro-react';
import React, { StrictMode, Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { getCookieConsentValue } from 'react-cookie-consent';
import { notFoundRoute } from './components/ErrorPage';
import App from './container/app';
import { modelsRoutes } from './container/models/routes';
import { store } from './store/configureStore';

const enableGrafanaTracking = getCookieConsentValue('rbit-tracking');

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      modelsRoutes,
      notFoundRoute,
    ],
  },
]);

if (enableGrafanaTracking === 'true') {
  initializeFaro({
    // required: the URL of the Grafana collector
    url: 'https://telemetry.oss.radicalbit.ai',
    apiKey: 'rbitoss-JpIYMVC677edETUbJN9Me3iLS7ngGaE2RYLzQWCOYVljUJh5JJk5o2FE',

    // required: the identification label of your application
    app: {
      name: 'radicalbit-ai-monitoring',
    },
  });
}

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
