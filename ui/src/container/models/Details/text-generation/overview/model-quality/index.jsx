import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCompletionModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { memo } from 'react';

function TextGenerationModelQualityMetrics() {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return 'ABEMUS PAPAM';
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(TextGenerationModelQualityMetrics);
