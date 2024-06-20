export const columnFactory = ({
  key,
  activeFilters,
  activeSorter,
  ...others
}) => ({
  key,
  defaultSortOrder: activeSorter && activeSorter[key],
  filteredValue: activeFilters && activeFilters[key],
  ...others,
});
