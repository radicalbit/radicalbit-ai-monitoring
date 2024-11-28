import contextConfigurationSlice from '@State/context-configuration';
import notificationSlice from '@State/notification';
import { apiService } from '@Store/apis';
import { configureStore } from '@reduxjs/toolkit';
import { rtkQueryErrorLogger, rtkQueryMutationSuccessLogger } from './middlewares';
import layoutSlice from './state/layout';
import globalConfigSlice from './state/global-configuration/slice';

const reducer = {
  contextConfiguration: contextConfigurationSlice,
  layout: layoutSlice,
  notification: notificationSlice,
  globalConfiguration: globalConfigSlice,
  [apiService.reducerPath]: apiService.reducer,

};

export const store = configureStore({
  reducer,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware()
    .concat(apiService.middleware)
    .concat(rtkQueryErrorLogger)
    .concat(rtkQueryMutationSuccessLogger),
});
