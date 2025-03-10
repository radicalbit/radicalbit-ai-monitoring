import { API_TAGS, apiService } from '@Src/store/apis';
import projectListMock from './mock/project-list.json';

export const tracingApiSlice = apiService.injectEndpoints({
  endpoints: (builder) => ({
    getTracingProjectByUUID: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.TRACING_PROJECT, id: uuid }],
      /* query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}`,
        method: 'get',
      }), */
      queryFn: (queryParams) => ({ data: projectListMock.list.find((t) => t.uuid === queryParams.uuid) }),
    }),

    addNewTracingProject: builder.mutation({
      invalidatesTags: (result) => {
        if (result) {
          return [API_TAGS.PROJECTS];
        }

        return [];
      },
      query: (data) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: '/models',
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

    getTracingProjects: builder.query({
      providesTags: [API_TAGS.PROJECTS],
      /*   query: ({ queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/project${queryParams ? `?${queryParams}` : ''}`,
        method: 'get',
      }), */
      queryFn: () => ({ data: projectListMock }),
    }),

  }),

});
