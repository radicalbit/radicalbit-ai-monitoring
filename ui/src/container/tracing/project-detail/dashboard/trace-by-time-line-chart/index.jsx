import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { tracingApiSlice } from '@State/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { Skeleton } from '@radicalbit/radicalbit-design-system';
import isEmpty from 'lodash/isEmpty';
import { useParams } from 'react-router-dom';
import { filtersToQueryParams } from '../filters';
import LineChart from './line-chart';

const {
  useGetTraceByTimeQuery,
} = tracingApiSlice;

function TraceByTimeLineChart() {
  const { uuid } = useParams();

  const { form } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;
  const toTimestamp = form?.toTimestamp;
  const queryParams = filtersToQueryParams(fromTimestamp, toTimestamp);

  const {
    data, isSuccess, isLoading, isError,
  } = useGetTraceByTimeQuery({ uuid, queryParams });
  const traces = data?.traces;

  if (isLoading) {
    return <Skeleton active paragraph={{ rows: 5 }} />;
  }

  if (isError) {
    return <SomethingWentWrong size="small" />;
  }

  if (isSuccess) {
    // e.g. 204 no content
    if (isEmpty(traces)) {
      return (
        <LineChart currentData={[]} />
      );
    }

    return (
      <LineChart currentData={traces} title="Traces by time" />
    );
  }

  return false;
}

export default TraceByTimeLineChart;
