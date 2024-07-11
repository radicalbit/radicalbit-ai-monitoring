import React, { StrictMode, Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { initializeFaro, withFaroRouterInstrumentation } from '@grafana/faro-react';
import { store } from './store/configureStore';
import { modelsRoutes } from './container/models/routes';
import App from './container/app';
import { notFoundRoute } from './components/ErrorPage';

initializeFaro({
  // required: the URL of the Grafana collector
  url: 'https://telemetry.oss.radicalbit.ai',

  // required: the identification label of your application
  app: {
    name: 'radicalbit-ai-monitoring',
  },
});

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

const browserRouter = withFaroRouterInstrumentation(router);

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
