import { JOB_STATUS } from '@Src/constants';
import { API_TAGS, apiService } from '@Src/store/apis';

export const modelsApiSlice = apiService.injectEndpoints({
  endpoints: (builder) => ({
    getModelByUUID: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.MODEL, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}`,
        method: 'get',
      }),
    }),

    addNewModel: builder.mutation({
      invalidatesTags: (result) => {
        if (result) {
          return [API_TAGS.MODELS];
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

    editModel: builder.mutation({
      invalidatesTags: (_, __, { data: { uuid } }) => [{ type: API_TAGS.MODEL, id: uuid }],
      query: ({ data }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${data.uuid}`,
        method: 'post',
        data,
      }),

    }),

    inferSchema: builder.mutation({
      query: ({ file, separator }) => {
        const data = new FormData();

        data.append('data_file', new File([file], file.name, { type: 'text/csv' }));
        data.append('separator', separator);

        return {
          baseUrl: import.meta.env.VITE_BASE_URL,
          url: '/schema/infer-schema',
          method: 'post',
          data,
        };
      },
    }),

    deleteModel: builder.mutation({
      invalidatesTags: [API_TAGS.MODELS, API_TAGS.OVERALL_STATS, API_TAGS.ALERTS, API_TAGS.OVERALL_MODELS],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}`,
        method: 'delete',
      }),
    }),

    getModels: builder.query({
      providesTags: [API_TAGS.MODELS],
      query: ({ queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models${queryParams ? `?${queryParams}` : ''}`,
        method: 'get',
      }),
    }),

    getReferenceDataQuality: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.REFERENCE_IMPORT, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/reference/data-quality`,
        method: 'get',
      }),
    }),

    getReferenceModelQuality: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.REFERENCE_IMPORT, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/reference/model-quality`,
        method: 'get',
      }),
    }),

    getReferenceImports: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.REFERENCE_IMPORT, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/reference`,
        method: 'get',
      }),
    }),

    importReferenceData: builder.mutation({
      query: ({ file, modelUUID }) => {
        const data = new FormData();

        data.append('model_uuid', modelUUID);
        data.append('csv_file', file);

        return ({
          baseUrl: import.meta.env.VITE_BASE_URL,
          url: `/models/${modelUUID}/reference/upload`,
          method: 'post',
          data,
          formData: true,
        });
      },
      invalidatesTags: (result, __, { modelUUID }) => {
        if (result) {
          return [
            { type: API_TAGS.REFERENCE_IMPORT, id: modelUUID },
            { type: API_TAGS.MODEL, id: modelUUID },
            { type: API_TAGS.MODELS },
          ];
        }
        return [];
      },
    }),

    getReferenceStatistics: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.REFERENCE_IMPORT, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/reference/statistics`,
        method: 'get',
      }),
    }),

    getCurrentStatisticsByUUID: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.CURRENT_IMPORT, id: uuid }],
      query: ({ uuid, currentUUID }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/current/${currentUUID}/statistics`,
        method: 'get',
      }),
    }),

    getCurrentDataQuality: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.CURRENT_IMPORT, id: uuid }],
      query: ({ uuid, currentUUID }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/current/${currentUUID}/data-quality`,
        method: 'get',
      }),
    }),

    getCurrentModelQuality: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.CURRENT_IMPORT, id: uuid }],
      query: ({ uuid, currentUUID }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/current/${currentUUID}/model-quality`,
        method: 'get',
      }),
    }),

    getCurrentImports: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.CURRENT_IMPORT, id: uuid }],
      query: ({ uuid, queryParams }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/current${queryParams ? `?${queryParams}` : ''}`,
        method: 'get',
      }),
    }),

    importCurrentData: builder.mutation({
      query: ({ file, modelUUID }) => {
        const data = new FormData();

        data.append('model_uuid', modelUUID);
        data.append('csv_file', file);

        return ({
          baseUrl: import.meta.env.VITE_BASE_URL,
          url: `/models/${modelUUID}/current/upload`,
          method: 'post',
          data,
          formData: true,
        });
      },
      invalidatesTags: (result, __, { modelUUID }) => {
        if (result) {
          return [
            { type: API_TAGS.CURRENT_IMPORT, id: modelUUID },
            { type: API_TAGS.MODEL, id: modelUUID },
            { type: API_TAGS.MODELS },
            { type: API_TAGS.OVERALL_MODELS },
          ];
        }
        return [];
      },
    }),

    getCurrentDrift: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.CURRENT_IMPORT, id: uuid }],
      query: ({ uuid, currentUUID }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/current/${currentUUID}/drift`,
        method: 'get',
      }),
    }),

    getOverallStats: builder.query({
      providesTags: () => [{ type: API_TAGS.OVERALL_STATS }],
      query: () => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: '/models/tot_percentages',
        method: 'get',
      }),
    }),

    getOverallModelList: builder.query({
      providesTags: () => [API_TAGS.OVERALL_MODELS],
      query: ({ limit }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/last_n?n_models=${limit}`,
        method: 'get',
      }),
      onQueryStarted: (async (arg, { queryFulfilled, dispatch }) => {
        const response = await queryFulfilled;

        if (response.data) {
          const isReferencePending = response.data.some((d) => d.latestReferenceJobStatus === JOB_STATUS.IMPORTING);
          const isCurrentPending = response.data.some((d) => d.latestCurrentJobStatus === JOB_STATUS.IMPORTING);
          const isPending = isReferencePending || isCurrentPending;

          if (!isPending) {
            dispatch(apiService.util.invalidateTags([API_TAGS.OVERALL_STATS, API_TAGS.ALERTS]));
          }
        }
      }),

    }),

    importCompletionData: builder.mutation({
      query: ({ file, modelUUID }) => {
        const data = new FormData();

        data.append('model_uuid', modelUUID);
        data.append('json_file', file);

        return ({
          baseUrl: import.meta.env.VITE_BASE_URL,
          url: `/models/${modelUUID}/completion/upload`,
          method: 'post',
          data,
          formData: true,
        });
      },
      invalidatesTags: (result, __, { modelUUID }) => {
        if (result) {
          return [
            { type: API_TAGS.COMPLETION_IMPORT, id: modelUUID },
            { type: API_TAGS.MODEL, id: modelUUID },
            { type: API_TAGS.MODELS },
            { type: API_TAGS.OVERALL_MODELS },

          ];
        }
        return [];
      },
    }),

    getCompletionImports: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.COMPLETION_IMPORT, id: uuid }],
      query: ({ uuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/completion`,
        method: 'get',
      }),
    }),

    getCompletionModelQuality: builder.query({
      providesTags: (_, __, { uuid }) => [{ type: API_TAGS.COMPLETION_IMPORT, id: uuid }],
      query: ({ uuid, latestCompletionUuid }) => ({
        baseUrl: import.meta.env.VITE_BASE_URL,
        url: `/models/${uuid}/completion/${latestCompletionUuid}/model-quality`,
        method: 'get',
      }),
    }),

  }),

});
