import TreeComponent from '@Components/modals/trace-detail-modal/tree';
import { Board, Spinner } from '@radicalbit/radicalbit-design-system';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useParams, useSearchParams } from 'react-router-dom';
import TraceDetail from './trace-detail';

const { useGetTraceDetailByUUIDQuery } = tracingApiSlice;

function Body() {
  const { uuid: projectUuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const traceUuid = searchParams.get('traceUuid');
  const spanId = searchParams.get('spanId');

  const { data: traceDetail, isLoading, isFetching } = useGetTraceDetailByUUIDQuery({ projectUuid, traceUuid });
  const defaultTreeSpanId = traceDetail?.tree.spanId;

  if (isLoading || isFetching || !defaultTreeSpanId) {
    return <Spinner />;
  }

  if (!spanId || spanId === null) {
    searchParams.set('spanId', defaultTreeSpanId);
    setSearchParams(searchParams);
  }

  return (
    <div className="flex flex-row h-full">
      <TreeComponent />

      <Board main={<TraceDetail />} modifier="w-full" />

    </div>
  );
}

export default Body;
