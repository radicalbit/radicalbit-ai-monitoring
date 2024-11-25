import { JOB_STATUS } from '@Src/constants';
import { Pin, Spinner } from '@radicalbit/radicalbit-design-system';

function JobStatusPin({ jobStatus }) {
  switch (jobStatus) {
    case JOB_STATUS.IMPORTING: {
      return (<Spinner fullHeight={false} fullWidth={false} size="small" spinning />);
    }

    case JOB_STATUS.ERROR: {
      return (<Pin size="small" type="error">{JOB_STATUS.ERROR}</Pin>);
    }

    case JOB_STATUS.MISSING_CURRENT: {
      return <Pin size="small" type="secondary" />;
    }

    case JOB_STATUS.MISSING_REFERENCE: {
      return <Pin size="small" type="secondary" />;
    }

    default:
      return <Pin size="small" type="primary" />;
  }
}

export default JobStatusPin;
