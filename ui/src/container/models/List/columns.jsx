import JobStatusPin from '@Components/JobStatus/job-status-pin';
import getJobStatus from '@Helpers/get-spinner-job-status';
import { columnFactory } from '@Src/components/smart-table/utils';
import { numberFormatter } from '@Src/constants';
import { DataTypeEnumLabel, ModelTypeEnumLabel } from '@State/models/constants';
import { RelativeDateTime } from '@radicalbit/radicalbit-design-system';

export const getColumns = (
  activeFilters,
  activeSorter,
) => [
  columnFactory({
    title: 'S',
    key: 'name',
    width: '3rem',
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
    width: 250,
    render: ({ uuid, name }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        <a className="pointer-events-none" href={`/models/${uuid}`}>
          {name}
        </a>
      </div>
    ),
  }),

  columnFactory({
    title: 'Model Type',
    dataIndex: 'modelType',
    key: 'modelType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: 200,
    render: (type) => <div>{ModelTypeEnumLabel[type]}</div>,
  }),

  columnFactory({
    title: 'Data Type',
    dataIndex: 'dataType',
    key: 'dataType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: 200,
    render: (type) => <div>{DataTypeEnumLabel[type]}</div>,
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
      const data = (value && value !== -1) ? `${numberFormatter({ maximumSignificantDigits: 4 }).format(parseFloat(value).toFixed(4) * 100)}%` : '--';

      return (
        <div>{data}</div>
      );
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
      const data = (value && value !== -1) ? `${numberFormatter({ maximumSignificantDigits: 4 }).format(parseFloat(value).toFixed(4) * 100)}%` : '--';

      return (
        <div>{data}</div>
      );
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
      const data = (value && value !== -1) ? `${numberFormatter({ maximumSignificantDigits: 4 }).format(parseFloat(value).toFixed(4) * 100)}%` : '--';

      return (
        <div>{data}</div>
      );
    },
  }),

  columnFactory({
    title: 'Created',
    dataIndex: 'createdAt',
    key: 'createdAt',
    activeFilters,
    activeSorter,
    align: 'right',
    width: '15%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),

  columnFactory({
    title: 'Updated',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
    activeFilters,
    activeSorter,
    sorter: true,
    align: 'right',
    width: '15%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),
];
