import { API_TAGS, apiService } from '@Src/store/apis';
import projectListMock from './mock/project-list.json';

export const tracingApiSlice = apiService.injectEndpoints({
  endpoints: (builder) => ({
    getProjectByUUID: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.TRACING_PROJECT, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/projects/${uuid}`,
        method: 'get',
      }),
    }),

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
      invalidatesTags: (_, __, { data: { uuid } }) => [{ type: API_TAGS.TRACING_PROJECT, id: uuid }],
      query: ({ data }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${data.uuid}`,
        method: 'post',
        data,
      }),

    }),

    deleteTracingProject: builder.mutation({
      invalidatesTags: [API_TAGS.PROJECTS],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}`,
        method: 'delete',
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

  }),

});
