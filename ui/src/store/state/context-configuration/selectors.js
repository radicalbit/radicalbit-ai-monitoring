import { SortOrderEnum, startPage } from '@Src/constants';
import { createDraftSafeSelector } from '@reduxjs/toolkit';
import flatten from 'lodash/flatten';
import isEmpty from 'lodash/isEmpty';

const selectQueryParamsSelector = createDraftSafeSelector(
  ({ contextConfiguration }, namespace) => contextConfiguration[namespace].pagination,
  ({ contextConfiguration }, namespace) => contextConfiguration[namespace].sorter,
  ({ contextConfiguration }, namespace) => contextConfiguration[namespace].filters,
  ({ contextConfiguration }, namespace) => contextConfiguration[namespace].externalFilters,
  (_, __, fn) => fn,
  (pagination, sorter, filters, externalFilters, fn) => {
    const paginationQuery = !pagination ? ''
      : `_page=${pagination.current || startPage}${pagination.pageSize ? `&_limit=${pagination.pageSize}` : ''}`;

    const sorterKey = sorter && Object.keys(sorter)[0];
    const sorterDirection = sorterKey && sorter[sorterKey];

    const sorterQuery = !sorterKey || !sorterDirection ? ''
      : `&_sort=${sorterKey}&_order=${sorterDirection.toLowerCase() === SortOrderEnum.ASCEND ? 'asc' : 'desc'}`;

    const filterQuery = isEmpty(filters) ? '' : `&${flatten(
      Object.keys(filters)
        .map((key) => filters[key]
          .map((x) => ({ [key]: x }))),
    )
      .map((x) => `${Object.keys(x)[0]}=${Object.values(x)[0]}`)
      .join('&')}`;

    const extrenaFiltersQuery = fn ? fn(externalFilters) : '';

    return `${paginationQuery}${sorterQuery}${filterQuery}${extrenaFiltersQuery ? `&${extrenaFiltersQuery}` : ''}`;
  },
);

const selectContextConfiguration = (
  { contextConfiguration },
  namespace,
) => contextConfiguration[namespace];

export default {
  selectQueryParamsSelector,
  selectContextConfiguration,
};
