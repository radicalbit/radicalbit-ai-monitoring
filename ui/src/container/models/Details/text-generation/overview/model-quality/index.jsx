import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCompletionModelQualityQueryWithPolling } from '@State/models/polling-hook';
import { memo } from 'react';
import { FormbitContextProvider } from '@radicalbit/formbit';
import TextGenerationFeatureList from './feature-list';
import BoardRow from './board-row';
import SearchFeatureList from './search-filter';

const initialValues = {
  __metadata: {
    searchToken: '',
  },
};

function TextGenerationModelQualityMetrics() {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const jobStatus = data?.jobStatus;

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <FormbitContextProvider initialValues={initialValues}>
        <div className="flex flex-col gap-4 p-4 h-full">
          <BoardRow />

          <SearchFeatureList />

          <TextGenerationFeatureList />
        </div>
      </FormbitContextProvider>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(TextGenerationModelQualityMetrics);
