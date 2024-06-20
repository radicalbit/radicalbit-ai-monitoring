import { useParams, useSearchParams } from 'react-router-dom';
import { modelsApiSlice } from '@State/models/api';
import NotFound from '@Components/ErrorPage/not-found';
import { MODEL_TABS_ENUM } from './constants';
import CurrentDashboard from './current-dashboard';
import Overview from './overview';
import ReferenceDashboard from './reference-dashboard';

const { useGetModelByUUIDQuery } = modelsApiSlice;

export function ModelDetails() {
  const { uuid } = useParams();

  const [searchParams] = useSearchParams();
  const activeKey = searchParams.get('tab') || MODEL_TABS_ENUM.OVERVIEW;

  const { error } = useGetModelByUUIDQuery({ uuid });
  const status = error?.status;

  if (status === 404) {
    return <NotFound />;
  }

  if (activeKey === MODEL_TABS_ENUM.OVERVIEW) {
    return (<Overview />);
  }

  if (activeKey === MODEL_TABS_ENUM.REFERENCE_DASHBOARD) {
    return (<ReferenceDashboard />);
  }

  if (activeKey === MODEL_TABS_ENUM.CURRENT_DASHBOARD) {
    return (<CurrentDashboard />);
  }
}
