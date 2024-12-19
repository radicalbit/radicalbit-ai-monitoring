import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCompletionModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { memo } from 'react';
import { FormbitContextProvider } from '@radicalbit/formbit';
import TextGenerationFeatureList from './feature-list';

const initialValues = {
  __metadata: {
    selectedFeatures: [],
  },
};

function TextGenerationModelQualityMetrics() {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <FormbitContextProvider initialValues={initialValues}>
        <div className="flex flex-col gap-4 p-4 h-full">
          <TextGenerationFeatureList />
        </div>
      </FormbitContextProvider>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(TextGenerationModelQualityMetrics);
