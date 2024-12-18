import NotFound from '@Components/ErrorPage/not-found';
import { MODEL_TABS_ENUM } from '@Container/models/Details/constants';
import { modelsApiSlice } from '@State/models/api';
import { useParams, useSearchParams } from 'react-router-dom';
import Overview from './overview';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function TextGenerationMetrics() {
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
}

export default TextGenerationMetrics;
