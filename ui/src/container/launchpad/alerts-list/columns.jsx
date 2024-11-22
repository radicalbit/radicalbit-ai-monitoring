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
    width: '4rem',
    align: 'center',
    render: () => (
      <JobStatusPin jobStatus={JOB_STATUS.ERROR} />
    ),
  }),
  columnFactory({
    title: 'Name',
    key: 'modelName',
    activeFilters,
    activeSorter,
    width: '35rem',
    render: ({ modelName }) => (
      <div className="font-[var(--coo-font-weight-bold)] w-96">
        <Truncate>{modelName}</Truncate>
      </div>
    ),
  }),
  columnFactory({
    title: 'Section',
    key: 'anomalyType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '20rem',
    render: ({ anomalyType }) => (<div>{METRICS_TABS[`${anomalyType}`]}</div>),
  }),

  columnFactory({
    title: 'Features with anomalies',
    key: 'anomalyFeatures',
    activeFilters,
    activeSorter,
    align: 'left',
    render: ({ anomalyFeatures }) => <div>{anomalyFeatures.join(', ')}</div>,
  }),

];
