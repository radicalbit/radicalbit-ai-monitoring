import useModals from '@Hooks/use-modals';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { useParams } from 'react-router';

const {
  useGetModelByUUIDQuery,
  useGetCurrentDataQualityQuery,
  useGetCurrentDriftQuery,
  useGetCurrentModelQualityQuery,
} = modelsApiSlice;

const useGetCurrentDataQuality = () => {
  const { uuid } = useParams();

  const { modalPayload: { data } } = useModals();
  const currentUUIDFromRow = data?.uuid;

  const { data: modelData } = useGetModelByUUIDQuery({ uuid }, { skip: currentUUIDFromRow });
  const currentUUIDFromModel = modelData?.currentLatestUUID;

  const currentUUID = currentUUIDFromRow || currentUUIDFromModel;

  return useGetCurrentDataQualityQuery({ uuid, currentUUID });
};

const useGetCurrentModelQuality = () => {
  const { uuid } = useParams();

  const { modalPayload: { data } } = useModals();
  const currentUUIDFromRow = data?.uuid;

  const { data: modelData } = useGetModelByUUIDQuery({ uuid }, { skip: currentUUIDFromRow });
  const currentUUIDFromModel = modelData?.currentLatestUUID;
  const currentUUID = currentUUIDFromRow || currentUUIDFromModel;

  return useGetCurrentModelQualityQuery({ uuid, currentUUID });
};

const useGetCurrentDrift = () => {
  const { uuid } = useParams();

  const { modalPayload: { data } } = useModals();
  const currentUUIDFromRow = data?.uuid;

  const { data: modelData } = useGetModelByUUIDQuery({ uuid }, { skip: currentUUIDFromRow });
  const currentUUIDFromModel = modelData?.currentLatestUUID;

  const currentUUID = currentUUIDFromRow || currentUUIDFromModel;

  return useGetCurrentDriftQuery({ uuid, currentUUID });
};

export {
  useGetCurrentDataQuality,
  useGetCurrentModelQuality,
  useGetCurrentDrift,
};
