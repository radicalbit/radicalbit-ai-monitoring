import {
  NamespaceEnum,
  SortOrderEnum,
  pageSize, startPage,
} from '@Src/constants';
import { createSlice } from '@reduxjs/toolkit';
import { isEmpty } from 'lodash';
import { queryString2configuration } from './utils';
import thunks from './thunks';

const { changeContextConfiguration } = thunks;

const defaultState = (
  customPageSize = pageSize,
  sorter = { updatedAt: SortOrderEnum.DESCEND },
  filters = {},
) => ({
  pagination: {
    current: startPage,
    pageSize: customPageSize,
    total: 0,
    showQuickJumper: true,
  },
  sorter,
  filters,
});

export const initialState = {
  [NamespaceEnum.MODELS]: defaultState(),
  [NamespaceEnum.MODELS_STATS]: defaultState(),
  [NamespaceEnum.CURRENT_IMPORT]: defaultState(pageSize, { date: SortOrderEnum.DESCEND }),
  [NamespaceEnum.REFERENCE_IMPORT]: defaultState(),
  [NamespaceEnum.COMPLETION_IMPORT]: defaultState(pageSize, { date: SortOrderEnum.DESCEND }),
  [NamespaceEnum.ALERTS]: defaultState(),
  [NamespaceEnum.MODELS_WIP]: defaultState(),
};

export const contextConfigurationSlice = createSlice({
  name: 'contextConfiguration',
  initialState,
  reducers: {
    clearPagination: (state, { payload }) => ({
      ...state,
      [payload.namespace]:
        {
          ...state[payload.namespace],
          pagination: defaultState().pagination,
        },
    }),

    clearFilters: (state, { payload }) => ({
      ...state,
      [payload.namespace]: {
        ...state[payload.namespace],
        filters: defaultState().filters,
      },
    }),

    clearSorter: (state, { payload }) => ({
      ...state,
      [payload.namespace]: {
        ...state[payload.namespace],
        sorter: defaultState().sorter,
      },
    }),

    setRawConfiguration: (state, { payload }) => isEmpty(payload.override)
      ? { ...initialState }
      : { ...state, ...payload.override },

    setRawConfigurationFromQueryString: (state, { payload }) => ({
      ...state,
      [payload.namespace]: queryString2configuration(payload.namespace, payload.queryString),
    }),
  },
  extraReducers: (builder) => {
    builder
      .addCase(changeContextConfiguration.pending, () => {})
      .addCase(changeContextConfiguration.fulfilled, (state, { payload }) => {
        if (payload) {
          Object.assign(state, { ...state, ...payload });
        }
      })
      .addCase(changeContextConfiguration.rejected, () => {});
  },
});

export const { actions } = contextConfigurationSlice;

export default contextConfigurationSlice.reducer;
