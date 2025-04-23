import { API_TAGS, apiService } from '@Src/store/apis';

export const tracingApiSlice = apiService.injectEndpoints({
  endpoints: (builder) => ({
    addNewProject: builder.mutation({
      invalidatesTags: (result) => {
        if (result) {
          return [API_TAGS.PROJECTS];
        }

        return [];
      },
      query: (data) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: '/projects',
        method: 'post',
        data,
      }),
    }),

    editTracingProject: builder.mutation({
      invalidatesTags: (_, __, { data: { uuid } }) => [
        { type: API_TAGS.TRACING_PROJECT, id: uuid },
      ],
      query: ({ uuid, name }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/projects/${uuid}`,
        method: 'post',
        data: { name },
      }),
    }),

    deleteProject: builder.mutation({
      invalidatesTags: [API_TAGS.PROJECTS],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/projects/${uuid}`,
        method: 'delete',
      }),
    }),

    getProjectByUUID: builder.query({
      providesTags: (_, __, { uuid }) => [
        { type: API_TAGS.TRACING_PROJECT, id: uuid },
      ],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/projects/${uuid}`,
        method: 'get',
      }),
    }),

    getAllProject: builder.query({
      providesTags: [API_TAGS.PROJECTS],
      query: () => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: '/projects/all',
        method: 'get',
      }),
    }),

    getSessionsByProjectUUID: builder.query({
      providesTags: (_, __, { uuid }) => [
        { type: API_TAGS.SESSIONS, id: uuid },
      ],
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/project/${uuid}/session${queryParams ? `?${queryParams}` : ''}`,
        method: 'get',
      }),
    }),

    getTracesByProjectUUID: builder.query({
      providesTags: (_, __, { uuid }) => [
        { type: API_TAGS.TRACE_LIST, id: uuid },
      ],
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/project/${uuid}/trace${queryParams ? `?${queryParams}` : ''}`,
        method: 'get',
      }),
    }),

    getTraceDetailByUUID: builder.query({
      providesTags: (_, __, { uuid }) => [
        { type: API_TAGS.TRACE_DETAIL, id: uuid },
      ],
      query: ({ projectUuid, traceUuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/project/${projectUuid}/trace/${traceUuid}`,
        method: 'get',
      }),
    }),

    getSpanDetailByUUID: builder.query({
      providesTags: (_, __, { spanId }) => [
        { type: API_TAGS.SPAN_DETAIL, id: spanId },
      ],
      query: ({ projectUuid, traceUuid, spanId }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/project/${projectUuid}/trace/${traceUuid}/span/${spanId}`,
        method: 'get',
      }),
    }),

    getTraceLatencies: builder.query({
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/dashboard/project/${uuid}/root-latencies?${queryParams}`,
        method: 'get',
      }),
    }),

    getSessionLatencies: builder.query({
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/dashboard/project/${uuid}/root-latencies-session?${queryParams}`,
        method: 'get',
      }),
    }),

    getSpanLatencies: builder.query({
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/dashboard/project/${uuid}/leaf-latencies?${queryParams}`,
        method: 'get',
      }),
    }),

    getTraceByTime: builder.query({
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/dashboard/project/${uuid}/trace-by-time?n=15&${queryParams}`,
        method: 'get',
      }),
    }),

    getApiKeyList: builder.query({
      providesTags: [API_TAGS.API_KEY],
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/api-key/project/${uuid}?${queryParams}`,
        method: 'get',
      }),
    }),

    deleteApiKey: builder.mutation({
      invalidatesTags: [API_TAGS.API_KEY],
      query: ({ uuid, apiKeyName }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/api-key/project/${uuid}/api-keys/${apiKeyName}`,
        method: 'delete',
      }),
    }),

    addNewApiKey: builder.mutation({
      invalidatesTags: (result) => {
        if (result) {
          return [API_TAGS.API_KEY];
        }

        return [];
      },
      query: ({ uuid, data }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/api-key/project/${uuid}`,
        method: 'post',
        data,
      }),
    }),

    getTracesBySession: builder.query({
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/dashboard/project/${uuid}/traces-by-session?${queryParams}`,
        method: 'get',
      }),
    }),
  }),
});
