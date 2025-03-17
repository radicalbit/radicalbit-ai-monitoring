import { JOB_STATUS } from '@Src/constants';
import { ModelTypeEnum } from '@State/models/constants';

const getJobStatus = ({
  modelType, latestCurrentJobStatus, latestReferenceJobStatus, latestCompletionJobStatus,
}) => {
  switch (modelType) {
    case ModelTypeEnum.TEXT_GENERATION:
      return latestCompletionJobStatus;
    default:
      return latestReferenceJobStatus === JOB_STATUS.SUCCEEDED ? latestCurrentJobStatus : latestReferenceJobStatus;
  }
};

export default getJobStatus;
