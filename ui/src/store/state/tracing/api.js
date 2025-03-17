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

  }),
});
