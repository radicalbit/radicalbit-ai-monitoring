import dayjs from 'dayjs';

export default function externalFiltersToQueryParams(externalFilters) {
  if (!externalFilters) {
    return '';
  }

  const { sessionUuid, fromTimestamp, toTimestamp } = externalFilters;

  const searchQueryParams = new URLSearchParams();

  if (sessionUuid !== null) {
    searchQueryParams.set('sessionUuid', sessionUuid);
  }

  if (fromTimestamp !== null) {
    searchQueryParams.set('fromTimestamp', dayjs(fromTimestamp).unix());
  }

  if (toTimestamp !== null) {
    searchQueryParams.set('toTimestamp', dayjs(toTimestamp).unix());
  }

  return searchQueryParams.toString();
}
