import { JOB_STATUS } from '@Src/constants';
import { useGetCurrentDataQualityQueryWithPolling, useGetReferenceDataQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { Pin, Spinner } from '@radicalbit/radicalbit-design-system';

function JobStatusPin({ modelUUID }) {
  const { data: referenceData } = useGetReferenceDataQualityQueryWithPolling(modelUUID);
  const referenceJobStatus = referenceData?.jobStatus;

  const { data: currentData } = useGetCurrentDataQualityQueryWithPolling(modelUUID);
  const currentJobStatus = currentData?.jobStatus;

  const jobStatus = (referenceJobStatus === JOB_STATUS.SUCCEEDED) ? currentJobStatus : referenceJobStatus;

  switch (jobStatus) {
    case JOB_STATUS.IMPORTING: {
      return (
        <Spinner
          fullHeight={false}
          fullWidth={false}
          size="small"
          spinning
        />

      );
    }

    case JOB_STATUS.ERROR: {
      return (
        <Pin size="small" type="filled-error">{JOB_STATUS.ERROR}</Pin>
      );
    }

    case JOB_STATUS.MISSING_REFERENCE: {
      return false;
    }

    default: return false;
  }
}

export default JobStatusPin;
