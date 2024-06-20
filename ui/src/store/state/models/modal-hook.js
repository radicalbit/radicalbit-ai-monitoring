import useModals from '@Hooks/use-modals';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { useParams } from 'react-router';

const {
  useGetCurrentDataQualityLatestQuery,
  useGetCurrentDataQualityQuery,
  useGetCurrentDriftLatestQuery,
  useGetCurrentDriftQuery,
  useGetCurrentModelQualityLatestQuery,
  useGetCurrentModelQualityQuery,
} = modelsApiSlice;

const useGetCurrentDataQuality = () => {
  const { uuid } = useParams();
  const { modalPayload: { data } } = useModals();

  const currentUUID = data?.uuid;

  const currentLatestResponse = useGetCurrentDataQualityLatestQuery({ uuid }, { skip: currentUUID });
  const currentResponse = useGetCurrentDataQualityQuery({ uuid, currentUUID }, { skip: !currentUUID });

  return (currentUUID) ? currentResponse : currentLatestResponse;
};

const useGetCurrentModelQuality = () => {
  const { uuid } = useParams();
  const { modalPayload: { data } } = useModals();

  const currentUUID = data?.uuid;

  const currentLatestResponse = useGetCurrentModelQualityLatestQuery({ uuid }, { skip: currentUUID });
  const currentResponse = useGetCurrentModelQualityQuery({ uuid, currentUUID }, { skip: !currentUUID });

  return currentUUID ? currentResponse : currentLatestResponse;
};

const useGetCurrentDrift = () => {
  const { uuid } = useParams();
  const { modalPayload: { data } } = useModals();

  const currentUUID = data?.uuid;

  const currentLatestResponse = useGetCurrentDriftLatestQuery({ uuid }, { skip: currentUUID });
  const currentResponse = useGetCurrentDriftQuery({ uuid, currentUUID }, { skip: !currentUUID });

  return (currentUUID) ? currentResponse : currentLatestResponse;
};

export {
  useGetCurrentDataQuality,
  useGetCurrentModelQuality,
  useGetCurrentDrift,
};
