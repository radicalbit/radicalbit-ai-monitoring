import JobStatusPin from '@Components/JobStatus/job-status-pin';
import { columnFactory } from '@Src/components/smart-table/utils';
import { JOB_STATUS } from '@Src/constants';

const columns = [
  columnFactory({
    title: 'S',
    key: 'name',
    width: '3rem',
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
    width: 250,
    render: ({ name }) => (<div className="font-[var(--coo-font-weight-bold)]">{name}</div>),
  }),
];

export default columns;
