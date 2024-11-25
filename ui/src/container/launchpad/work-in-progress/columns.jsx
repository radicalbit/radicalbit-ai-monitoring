import JobStatusPin from '@Components/JobStatus/job-status-pin';
import { RelativeDateTime, Truncate } from '@radicalbit/radicalbit-design-system';
import { columnFactory } from '@Src/components/smart-table/utils';
import { JOB_STATUS } from '@Src/constants';
import { ModelTypeEnumLabel } from '@Src/store/state/models/constants';

const columns = (
  activeFilters,
  activeSorter,
) => [
  columnFactory({
    title: 'S',
    key: 'name',
    width: '3%',
    align: 'center',
    render: ({ latestCurrentJobStatus, latestReferenceJobStatus }) => {
      const jobStatus = latestReferenceJobStatus === JOB_STATUS.SUCCEEDED
        ? latestCurrentJobStatus
        : latestReferenceJobStatus;

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
    render: ({ name }) => (
      <div className="font-[var(--coo-font-weight-bold)] w-96">
        <Truncate>{name}</Truncate>
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
    width: '51%',
    render: (type) => <div>{ModelTypeEnumLabel[type]}</div>,
  }),

  columnFactory({
    title: 'Updated',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
    activeFilters,
    activeSorter,
    sorter: true,
    align: 'right',
    width: '13%',
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),
];

export default columns;
