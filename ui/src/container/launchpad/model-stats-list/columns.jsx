import JobStatusPin from '@Components/JobStatus/job-status-pin';
import getJobStatus from '@Helpers/get-spinner-job-status';
import { columnFactory } from '@Src/components/smart-table/utils';
import { numberFormatter } from '@Src/constants';
import { ModelTypeEnumLabel } from '@State/models/constants';
import { RelativeDateTime, Truncate } from '@radicalbit/radicalbit-design-system';

export const getColumns = (
  activeFilters,
  activeSorter,
) => [
  columnFactory({
    title: 'S',
    key: 'name',
    width: '3%',
    align: 'center',
    render: ({
      modelType, latestCurrentJobStatus, latestReferenceJobStatus, latestCompletionJobStatus,
    }) => {
      const jobStatus = getJobStatus({
        modelType, latestCurrentJobStatus, latestReferenceJobStatus, latestCompletionJobStatus,
      });
      return (
        <JobStatusPin jobStatus={jobStatus} />
      );
    },
  }),
  columnFactory({
    title: 'Name',
    key: 'name',
    activeFilters,
    activeSorter,
    width: '33%',
    render: ({ uuid, name }) => (
      <a
        className="font-[var(--coo-font-weight-bold)]"
        href={`/models/${uuid}`}
        onClick={(e) => e.preventDefault()}
      >
        <Truncate>{name}</Truncate>
      </a>
    ),
  }),

  columnFactory({
    title: 'Model Type',
    dataIndex: 'modelType',
    key: 'modelType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '21%',
    render: (type) => <div>{ModelTypeEnumLabel[type]}</div>,
  }),

  columnFactory({
    title: 'Data Quality',
    key: 'dataQuality',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '10%',
    render: ({ percentages }) => {
      const value = percentages?.dataQuality.value;
      const data = (value && value !== -1) ? `${numberFormatter({ maximumSignificantDigits: 4 }).format(parseFloat(value) * 100)}%` : '--';

      return data;
    },
  }),

  columnFactory({
    title: 'Model Quality',
    key: 'modelQuality',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '10%',
    render: ({ percentages }) => {
      const value = percentages?.modelQuality.value;
      const data = (value && value !== -1) ? `${numberFormatter({ maximumSignificantDigits: 4 }).format(parseFloat(value) * 100)}%` : '--';

      return data;
    },
  }),

  columnFactory({
    title: 'Drift Quality',
    key: 'driftQuality',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '10%',
    render: ({ percentages }) => {
      const value = percentages?.drift.value;
      const data = (value && value !== -1) ? `${numberFormatter({ maximumSignificantDigits: 4 }).format(parseFloat(value) * 100)}%` : '--';

      return data;
    },
  }),

  columnFactory({
    title: 'Updated',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
    activeFilters,
    activeSorter,
    sorter: false,
    align: 'right',
    width: '13%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),
];
