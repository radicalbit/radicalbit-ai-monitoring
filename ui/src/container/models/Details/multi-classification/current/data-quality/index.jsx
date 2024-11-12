import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCurrentDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { FormbitContextProvider } from '@radicalbit/formbit';
import { Spinner } from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import DataPointDistribution from './data-point-distribution';
import SearchFeatureList from './search-filter';
import DataQualityList from './data-quality-list';

const initialValues = {
  __metadata: {
    selectedFeatures: [],
    isNumericalSelected: true,
    isCategoricalSelected: true,
  },
};

function MultiClassificationDataQualityMetrics() {
  const { data, isError, isLoading } = useGetCurrentDataQualityQueryWithPolling();
  const jobStatus = data?.jobStatus;

  if (isLoading) {
    return <Spinner spinning />;
  }

  if (isError) {
    return <SomethingWentWrong />;
  }

  if (!data) {
    return <JobStatus jobStatus={JOB_STATUS.MISSING_CURRENT} />;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <FormbitContextProvider initialValues={initialValues}>

        <div className="flex flex-col gap-4 p-4 h-full">
          <DataPointDistribution />

          <SearchFeatureList />

          <DataQualityList />
        </div>

      </FormbitContextProvider>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(MultiClassificationDataQualityMetrics);
