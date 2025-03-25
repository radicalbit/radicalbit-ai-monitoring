import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetReferenceDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { FormbitContextProvider } from '@radicalbit/formbit';
import { memo } from 'react';
import { useParams } from 'react-router-dom';
import DataPointDistribution from './data-point-distribution';
import SearchFeatureList from './search-filter';
import DataQualityList from './data-quality-list';

const { useGetReferenceDataQualityQuery } = modelsApiSlice;

const initialValues = {
  __metadata: {
    selectedFeatures: [],
    isNumericalSelected: true,
    isCategoricalSelected: true,
  },
};

function BinaryClassificationDataQualityMetrics() {
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

export default memo(BinaryClassificationDataQualityMetrics);
