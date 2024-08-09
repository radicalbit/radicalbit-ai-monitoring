import { notificationErrorJson } from '@Helpers/notificationUtils';
import { qsSetEncode64JSON } from '@Helpers/queryParams';
import { actions as notificationActions } from '@State/notification';
import { createAsyncThunk } from '@reduxjs/toolkit';
import { isEqual } from 'lodash';
import { grafanaTracking } from '@Src/main';
import contextConfigurationSelectors from './selectors';

const { selectContextConfiguration } = contextConfigurationSelectors;

const { setNotificationMessage } = notificationActions;

const storeConfigInUrl = (configuration) => {
  const newQS = configuration ? qsSetEncode64JSON('configuration', configuration) : '';
  const newUrl = `${window.location.pathname}?${newQS}`;

  window.history.pushState({ path: newUrl }, '', newUrl);
};

const changeContextConfiguration = createAsyncThunk(
  'contextConfiguration/changeContextConfiguration',
  async ({ namespace, configuration }, {
    getState, fulfillWithValue, dispatch, rejectWithValue,
  }) => {
    try {
      const {
        pagination, sorter, filters,
      } = configuration;

      const old = selectContextConfiguration(getState(), namespace);

      const filtersChanged = !isEqual(filters, old?.filters);

      const newConfigurationForNamespace = {
        pagination: filtersChanged ? { ...pagination, current: 1 } : pagination,
        sorter,
        filters,
      };
      const newConfiguration = { [namespace]: newConfigurationForNamespace };

      storeConfigInUrl(newConfiguration);

      return fulfillWithValue(newConfiguration);
    } catch (e) {
      console.error(e);
      grafanaTracking?.api.pushError(e);
      const notificationMessage = notificationErrorJson(e);
      dispatch(setNotificationMessage(notificationMessage));

      return rejectWithValue(e);
    }
  },
);

export default { changeContextConfiguration };
