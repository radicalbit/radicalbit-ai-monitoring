import { API_TAGS, apiService } from '@Src/store/apis';

export const alertsApiSlice = apiService.injectEndpoints({
  endpoints: (builder) => ({
    getAlerts: builder.query({
      providesTags: () => [{ type: API_TAGS.ALERTS }],
      query: () => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: '/alerts',
        method: 'get',
      }),
    }),
  }),
});