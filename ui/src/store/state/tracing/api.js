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
      query: ({ data }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${data.uuid}`,
        method: 'post',
        data,
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
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/session/all/${uuid}`,
        method: 'get',
      }),
    }),

    getTracesByProjectUUID: builder.query({
      providesTags: (_, __, { uuid }) => [
        { type: API_TAGS.TRACE_LIST, id: uuid },
      ],
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/traces/project/${uuid}${queryParams ? `?${queryParams}` : ''}`,
        method: 'get',
      }),
    }),

    getTraceLatencies: builder.query({
      // providesTags: TODO
      queryFn: () => ({
        data: [{
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: null,
          p50Ms: 240.596499,
          p90Ms: 4077.859945800001,
          p95Ms: 5651.5162593999985,
          p99Ms: 6910.44131028,
        }],
      }),
    }),

    getSessionLatencies: builder.query({
      // providesTags: TODO
      queryFn: () => ({
        data: [{
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: '00000000-0000-0000-0000-000000000092',
          spanName: null,
          p50Ms: 240.596499,
          p90Ms: 4077.859945800001,
          p95Ms: 5651.5162593999985,
          p99Ms: 6910.44131028,
        }],
      }),
    }),

    getSpanLatencies: builder.query({
      // providesTags: TODO
      queryFn: () => ({
        data: [{
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'ChannelWrite<start:agent>.task',
          p50Ms: 0.589038,
          p90Ms: 0.589038,
          p95Ms: 0.589038,
          p99Ms: 0.589038,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'smart-model-langgraph-app_00000000-0000-0000-0000-000000000003.chat',
          p50Ms: 3244.985058,
          p90Ms: 4032.925578,
          p95Ms: 4131.418143,
          p99Ms: 4210.212195,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'should_continue.task',
          p50Ms: 0.741633,
          p90Ms: 0.8956634,
          p95Ms: 0.9149172,
          p99Ms: 0.93032024,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'wikipedia.tool',
          p50Ms: 1819.426915,
          p90Ms: 1819.426915,
          p95Ms: 1819.426915,
          p99Ms: 1819.426915,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'ChannelWrite<...>.task',
          p50Ms: 0.600514,
          p90Ms: 0.600514,
          p95Ms: 0.600514,
          p99Ms: 0.600514,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'ChannelWrite<...,ask_human>.task',
          p50Ms: 1.106528,
          p90Ms: 1.106528,
          p95Ms: 1.106528,
          p99Ms: 1.106528,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'ChannelWrite<...,agent>.task',
          p50Ms: 0.732713,
          p90Ms: 0.7566498,
          p95Ms: 0.7596419,
          p99Ms: 0.7620355799999999,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'ChannelWrite<...,action>.task',
          p50Ms: 0.808036,
          p90Ms: 0.808036,
          p95Ms: 0.808036,
          p99Ms: 0.808036,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'ask_human.task',
          p50Ms: 4.802592,
          p90Ms: 4.802592,
          p95Ms: 4.802592,
          p99Ms: 4.802592,
        }, {
          projectUuid: '00000000-0000-0000-0000-000000000003',
          sessionUuid: null,
          spanName: 'GET',
          p50Ms: 228.159651,
          p90Ms: 339.98420860000004,
          p95Ms: 366.0241033,
          p99Ms: 386.85601906,
        }],
      }),
    }),
  }),
});
