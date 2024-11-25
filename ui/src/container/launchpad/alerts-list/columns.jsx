import JobStatusPin from '@Components/JobStatus/job-status-pin';
import { METRICS_TABS } from '@Container/models/Details/constants';
import { columnFactory } from '@Src/components/smart-table/utils';
import { JOB_STATUS } from '@Src/constants';
import { Truncate } from '@radicalbit/radicalbit-design-system';

export const getColumns = (
  activeFilters,
  activeSorter,
) => [
  columnFactory({
    title: 'S',
    key: 'name',
    width: '3%',
    align: 'center',
    render: () => (
      <JobStatusPin jobStatus={JOB_STATUS.ERROR} />
    ),
  }),
  columnFactory({
    title: 'Section',
    key: 'anomalyType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '17%',
    render: ({ uuid, anomalyType }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        <a className="pointer-events-none" href={`/models/${uuid}`}>
          {METRICS_TABS[`${anomalyType}`]}
        </a>
      </div>
    ),
  }),

  columnFactory({
    title: 'Name',
    key: 'modelName',
    activeFilters,
    activeSorter,
    width: '16%',
    render: ({ modelName }) => (
      <div className="w-96">
        <Truncate>{modelName}</Truncate>
      </div>
    ),
  }),

  columnFactory({
    title: 'Features with anomalies',
    key: 'anomalyFeatures',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '64%',
    render: ({ anomalyFeatures }) => <div>{anomalyFeatures.join(', ')}</div>,
  }),

];
