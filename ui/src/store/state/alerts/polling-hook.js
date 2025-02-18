import { DEFAULT_POLLING_INTERVAL } from '@Src/constants';

import { alertsApiSlice } from './api';

const { useGetAlertsQuery } = alertsApiSlice;
const useGetModelsQueryWithPolling = () => useGetAlertsQuery(undefined, { pollingInterval: DEFAULT_POLLING_INTERVAL });

export {
  useGetModelsQueryWithPolling,
};
