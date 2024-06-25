import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCurrentDataQuality } from '@State/models/modal-hook';
import { useGetCurrentDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { FormbitContextProvider } from '@radicalbit/formbit';
import { memo } from 'react';
import DataPointDistribution from './data-point-distribution';
import DataQualityList from './data-quality-list';
import SearchFeatureList from './search-filter';

const initialValues = {
  __metadata: {
    selectedFeatures: [],
    isNumericalSelected: true,
    isCategoricalSelected: true,
  },
};

function BinaryClassificationMetrics() {
  useGetCurrentDataQualityQueryWithPolling();

  const { data, isError } = useGetCurrentDataQuality();

  const jobStatus = data?.jobStatus;

  if (isError) {
    return <SomethingWentWrong />;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <FormbitContextProvider initialValues={initialValues}>

        <div className="flex flex-col gap-4 py-4 h-full">
          <DataPointDistribution />

          <SearchFeatureList />

          <DataQualityList />
        </div>

      </FormbitContextProvider>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default memo(BinaryClassificationMetrics);
