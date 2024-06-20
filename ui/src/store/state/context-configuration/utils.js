import { SortOrderEnum } from '@Src/constants';
import { initialState } from '@State/context-configuration';
import isArray from 'lodash/isArray';
import isEmpty from 'lodash/isEmpty';
import qs from 'query-string';

const CURRENT_PAGE = '_page';
const PAGE_SIZE = '_limit';
const SORT = '_sort';
const SORT_ORDER_PARAM = '_order';

export const applyPaginationFiltersAndSorterToItem = (
  items,
  pagination,
  filters,
  sorter,
) => {
  const filtersKeys = Object.keys(filters);
  const sortKey = !isEmpty(sorter) && Object.keys(sorter)[0];
  const sortOrder = sortKey ? sorter[sortKey] : SortOrderEnum.ASCEND;

  const filtered = filtersKeys.length
    ? items
      .filter((item) => filtersKeys.reduce(
        (acc, key) => !(filters[key] ?? []).length
          ? acc && true
          : acc && (filters[key] ?? []).includes(item[key]),
        true,
      ))
    : items;

  const sortered = sortKey
    ? filtered.sort((a, b) => {
      const aL = a[sortKey].toString();
      const bL = b[sortKey].toString();
      const numeric = typeof a[sortKey] !== 'string';
      const sensitivity = 'base';
      return sortOrder?.toString().toLowerCase() === SortOrderEnum.ASCEND
        ? aL.localeCompare(bL, undefined, { numeric, sensitivity })
        : bL.localeCompare(aL, undefined, { numeric, sensitivity });
    })
    : filtered;

  const { current = 1, pageSize = 20 } = pagination;

  const start = (current - 1) * pageSize;
  const end = (current * pageSize);
  return sortered.slice(start, end);
};

export const queryString2configuration = (namespace, queryString) => {
  if (!queryString) {
    return initialState[namespace];
  }

  const parsed = qs.parse(queryString);
  const {
    [CURRENT_PAGE]: current,
    [PAGE_SIZE]: pageSize,
    [SORT]: sortName,
    [SORT_ORDER_PARAM]: sortOrder,
    ...other
  } = parsed;

  const pagination = current && pageSize && typeof current === 'string' && typeof pageSize === 'string'
    ? {
      current: parseInt(current, 10),
      pageSize: parseInt(pageSize, 10),
    }
    : initialState[namespace].pagination;

  const filters = Object.keys(other).reduce(
    (acc, key) => {
      const val = isArray(other[key]) ? other[key] : [other[key]];
      return { ...acc, [key]: val };
    },
    {},
  );

  const sorter = sortName && sortOrder && typeof sortName === 'string' && typeof sortOrder === 'string'
    ? { [sortName]: sortOrder.toLowerCase() === 'asc' ? SortOrderEnum.ASCEND : SortOrderEnum.DESCEND }
    : initialState[namespace].sorter;

  return { pagination, filters, sorter };
};
