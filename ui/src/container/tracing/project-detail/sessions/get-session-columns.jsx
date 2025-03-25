import { RelativeDateTime } from '@radicalbit/radicalbit-design-system';
import { columnFactory } from '@Src/components/smart-table/utils';

const getSessionColumns = (
  activeFilters,
  activeSorter,
) => [

  columnFactory({
    title: 'UUID',
    key: 'sessionUuid',
    activeFilters,
    activeSorter,
    render: ({ sessionUuid }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        {sessionUuid}
      </div>
    ),
  }),

  columnFactory({
    title: 'Traces',
    key: 'traces',
    dataIndex: 'traces',
    activeFilters,
    activeSorter,
  }),

  columnFactory({
    title: 'Errors',
    key: 'numberOfErrors',
    dataIndex: 'numberOfErrors',
    activeFilters,
    activeSorter,
  }),

  columnFactory({
    title: 'Completion tokens',
    key: 'completionTokens',
    dataIndex: 'completionTokens',
    activeFilters,
    activeSorter,
  }),

  columnFactory({
    title: 'Prompt tokens',
    key: 'promptTokens',
    dataIndex: 'promptTokens',
    activeFilters,
    activeSorter,
  }),

  columnFactory({
    title: 'Total Tokens',
    key: 'totalTokens',
    dataIndex: 'totalTokens',
    activeFilters,
    activeSorter,
  }),

  columnFactory({
    title: 'Created at',
    dataIndex: 'createdAt',
    key: 'createdAt',
    activeFilters,
    activeSorter,
    sorter: false,
    align: 'right',
    width: '13%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),

  columnFactory({
    title: 'Latest Trace at',
    dataIndex: 'latestTraceTs',
    key: 'latestTraceTs',
    activeFilters,
    activeSorter,
    sorter: false,
    align: 'right',
    width: '13%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),

];

export default getSessionColumns;
