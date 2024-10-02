import JobStatusPin from '@Components/JobStatus/job-status-pin';
import { columnFactory } from '@Src/components/smart-table/utils';
import { JOB_STATUS } from '@Src/constants';
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
    render: ({ latestCurrentJobStatus, latestReferenceJobStatus }) => {
      const jobStatus = latestReferenceJobStatus === JOB_STATUS.SUCCEEDED ? latestCurrentJobStatus : latestReferenceJobStatus;
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
    render: ({ name }) => (<div className="font-[var(--coo-font-weight-bold)]">{name}</div>),
  }),

  columnFactory({
    title: 'Model Type',
    dataIndex: 'modelType',
    key: 'modelType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: 200,
    render: (type) => <div className="font-[var(--coo-font-weight-bold)]">{ModelTypeEnumLabel[type]}</div>,
  }),

  columnFactory({
    title: 'Data Type',
    dataIndex: 'dataType',
    key: 'dataType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: 200,
    render: (type) => <div className="font-[var(--coo-font-weight-bold)]">{DataTypeEnumLabel[type]}</div>,
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
