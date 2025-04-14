import { customBaseQuery } from '@Api/utils';
import { createApi } from '@reduxjs/toolkit/query/react';

export const API_TAGS = {
  ALERTS: 'Alerts',
  MODELS: 'Models',
  MODEL: 'Model',
  REFERENCE_IMPORT: 'REFERENCE_IMPORT',
  CURRENT_IMPORT: 'CURRENT_IMPORT',
  OVERALL_MODELS: 'OVERALL_MODELS',
  OVERALL_STATS: 'OVERALL_STATS',
  COMPLETION_IMPORT: 'COMPLETION_IMPORT',
  PROJECTS: 'PROJECTS',
  PROJECT: 'PROJECT',
  SESSIONS: 'SESSIONS',
  TRACE_LIST: 'TRACE_LIST',
  TRACE_DETAIL: 'TRACE_DETAIL',
  SPAN_DETAIL: 'SPAN_DETAIL',
  API_KEY: 'API_KEY',
};

export const apiService = createApi({
  reducerPath: 'api',
  baseQuery: customBaseQuery(),
  tagTypes: [
    API_TAGS.MODELS,
    API_TAGS.MODEL,
  ],
  endpoints: () => ({}),
});
