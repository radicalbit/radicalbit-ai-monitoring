import NotFound from '@Components/ErrorPage/not-found';
import { modelsApiSlice } from '@State/models/api';
import { useParams, useSearchParams } from 'react-router-dom';
import { MODEL_TABS_ENUM } from '@Container/models/Details/constants';
import Current from './current';
import ReferenceDashboard from './reference';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function EmbeddingsMetrics() {
  const { uuid } = useParams();

  const [searchParams] = useSearchParams();
  const activeKey = searchParams.get('tab') || MODEL_TABS_ENUM.REFERENCE_DASHBOARD;

  const { error } = useGetModelByUUIDQuery({ uuid });
  const status = error?.status;

  if (status === 404) {
    return <NotFound />;
  }

  if (activeKey === MODEL_TABS_ENUM.REFERENCE_DASHBOARD) {
    return (<ReferenceDashboard />);
  }

  if (activeKey === MODEL_TABS_ENUM.CURRENT_DASHBOARD) {
    return (<Current />);
  }
}

export default EmbeddingsMetrics;
