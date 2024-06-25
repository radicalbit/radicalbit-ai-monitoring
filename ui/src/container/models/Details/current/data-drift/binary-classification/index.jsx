import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import JobStatus from '@Components/JobStatus';
import { JOB_STATUS } from '@Src/constants';
import { useGetCurrentDrift } from '@State/models/modal-hook';
import { useGetCurrentDriftQueryWithPolling } from '@State/models/polling-hook';
import { FormbitContextProvider } from '@radicalbit/formbit';
import DataDriftHeader from './header';
import DataDriftList from './list';
import SearchFeatureList from './search-filter';

const initialValues = {
  __metadata: {
    selectedFeatures: [],
    isNumericalSelected: true,
    isCategoricalSelected: true,
  },
};

function DataDriftMetrics() {
  useGetCurrentDriftQueryWithPolling();

  const { data, isError } = useGetCurrentDrift();

  const jobStatus = data?.jobStatus;

  if (isError) {
    return <SomethingWentWrong />;
  }

  if (jobStatus === JOB_STATUS.SUCCEEDED) {
    return (
      <FormbitContextProvider initialValues={initialValues}>
        <div className="flex flex-col gap-4 h-full">
          <DataDriftHeader />

          <SearchFeatureList />

          <DataDriftList />
        </div>
      </FormbitContextProvider>
    );
  }

  return (<JobStatus jobStatus={jobStatus} />);
}

export default DataDriftMetrics;
