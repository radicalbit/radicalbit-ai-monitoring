import { RelativeDateTime } from '@radicalbit/radicalbit-design-system';
import { columnFactory } from '@Src/components/smart-table/utils';
import { numberFormatter } from '@Src/constants';

export const getColumns = (
  activeFilters,
  activeSorter,
) => [

  columnFactory({
    title: 'UUID',
    key: 'traceId',
    activeFilters,
    activeSorter,
    render: ({ traceId }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        {traceId}
      </div>
    ),
  }),

  columnFactory({
    title: 'Durations',
    dataIndex: 'durationMs',
    key: 'durationMs',
    activeFilters,
    activeSorter,
    sorter: false,
    align: 'right',
    width: '13%',
    render: (date) => `${numberFormatter().format(date / 1000)}s`,
  }),

  columnFactory({
    title: 'Spans',
    key: 'spans',
    dataIndex: 'spans',
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
    title: 'Latest span',
    dataIndex: 'latestSpanTs',
    key: 'latestSpanTs',
    activeFilters,
    activeSorter,
    sorter: false,
    align: 'right',
    width: '13%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),

];
