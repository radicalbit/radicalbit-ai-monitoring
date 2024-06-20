import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetReferenceDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { FormbitContextProvider } from '@radicalbit/formbit';
import { memo } from 'react';
import { useParams } from 'react-router';
import DataPointDistribution from './data-point-distribution';
import DataQualityList from './data-quality-list';
import SearchFeatureList from './search-filter';

const { useGetReferenceDataQualityQuery } = modelsApiSlice;

const initialValues = {
  __metadata: {
    selectedFeatures: [],
    isNumericalSelected: true,
    isCategoricalSelected: true,
  },
};

function BinaryClassificationMetrics() {
  useGetReferenceDataQualityQueryWithPolling();
  const { uuid } = useParams();
  const { data, isError } = useGetReferenceDataQualityQuery({ uuid });
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
