import React, { StrictMode, Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { store } from './store/configureStore';
import { modelsRoutes } from './container/models/routes';
import App from './container/app';
import { notFoundRoute } from './components/ErrorPage';

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

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <Suspense fallback={<div />}>
        <StrictMode>
          <RouterProvider router={router} />
        </StrictMode>
      </Suspense>
    </Provider>
  </React.StrictMode>,
);
