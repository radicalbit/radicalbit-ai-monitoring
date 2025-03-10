import { columnFactory } from '@Src/components/smart-table/utils';

export const getColumns = (
  activeFilters,
  activeSorter,
) => [

  columnFactory({
    title: 'UUID',
    key: 'uuid',
    activeFilters,
    activeSorter,
    width: 250,
    render: ({ uuid }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        <a className="pointer-events-none" href={`/projects/${uuid}`}>
          {uuid}
        </a>
      </div>
    ),
  }),

  columnFactory({
    title: 'Name',
    key: 'name',
    activeFilters,
    activeSorter,
    width: 250,
    render: ({ name }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        {name}
      </div>
    ),
  }),

];
