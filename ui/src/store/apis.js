import { customBaseQuery } from '@Api/utils';
import { createApi } from '@reduxjs/toolkit/query/react';

export const API_TAGS = {
  MODELS: 'Models',
  MODEL: 'Model',
  REFERENCE_IMPORT: 'REFERENCE_IMPORT',
  CURRENT_IMPORT: 'CURRENT_IMPORT',
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
