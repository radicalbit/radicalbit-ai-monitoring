import { DEFAULT_POLLING_INTERVAL, JOB_STATUS, NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import useModals from '@Hooks/use-modals';
import { modelsApiSlice } from './api';

const {
  useGetReferenceImportsQuery,
  useGetReferenceDataQualityQuery,
  useGetReferenceModelQualityQuery,
  useGetReferenceStatisticsQuery,
  useGetCurrentImportsQuery,
  useGetCurrentDataQualityQuery,
  useGetCurrentModelQualityQuery,
  useGetCurrentStatisticsByUUIDQuery,
  useGetCurrentDriftQuery,
  useGetModelByUUIDQuery,
} = modelsApiSlice;

const useGetReferenceImportsQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetReferenceImportsQuery({ uuid });
  const status = data?.items[0]?.status;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceImportsQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });
};

const useGetReferenceDataQualityQueryWithPolling = (modelUUID) => {
  const { uuid: uuidFromUrl } = useParams();

  const uuid = modelUUID !== undefined ? modelUUID : uuidFromUrl;

  const result = useGetReferenceDataQualityQuery({ uuid });
  const status = result.data?.jobStatus;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceDataQualityQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });

  return result;
};

const useGetReferenceModelQualityQueryWithPolling = () => {
  const { uuid } = useParams();

  const result = useGetReferenceModelQualityQuery({ uuid });
  const status = result.data?.jobStatus;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceModelQualityQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });

  return result;
};

const useGetReferenceStatisticsQueryWithPolling = () => {
  const { uuid } = useParams();

  const result = useGetReferenceStatisticsQuery({ uuid });

  const status = result.data?.jobStatus;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceStatisticsQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });

  return result;
};

const useGetCurrentImportsQueryWithPolling = () => {
  const { uuid } = useParams();
  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.CURRENT_IMPORT));

  const result = useGetCurrentImportsQuery({ uuid, queryParams });
  const currentActiveImport = result.data?.items.filter((i) => i.status === JOB_STATUS.IMPORTING).length ?? 0;

  useGetCurrentImportsQuery({ uuid, queryParams }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: currentActiveImport === 0 });

  return result;
};

const useGetCurrentDataQualityQueryWithPolling = (modelUUID) => {
  const { uuid: uuidFromUrl } = useParams();

  const uuid = modelUUID !== undefined ? modelUUID : uuidFromUrl;

  const { modalPayload: { data: modalData } } = useModals();

  const { data: model } = useGetModelByUUIDQuery({ uuid }, { skip: modalData?.uuid });
  const latestCurrentUuid = model?.latestCurrentUuid;

  const currentUUID = modalData?.uuid !== undefined ? modalData.uuid : latestCurrentUuid;

  const result = useGetCurrentDataQualityQuery({ uuid, currentUUID }, { skip: !currentUUID });
  const status = result.data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentDataQualityQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });

  return result;
};

const useGetCurrentModelQualityQueryWithPolling = () => {
  const { uuid } = useParams();

  const { modalPayload: { data: modalData } } = useModals();

  const { data: model } = useGetModelByUUIDQuery({ uuid }, { skip: modalData?.uuid });
  const latestCurrentUuid = model?.latestCurrentUuid;

  const currentUUID = modalData?.uuid !== undefined ? modalData.uuid : latestCurrentUuid;

  const result = useGetCurrentModelQualityQuery({ uuid, currentUUID }, { skip: !currentUUID });
  const status = result.data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentModelQualityQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });

  return result;
};

const useGetCurrentStatisticsQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const currentUUID = model?.latestCurrentUuid;

  const result = useGetCurrentStatisticsByUUIDQuery({ uuid, currentUUID });
  const status = result.data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentStatisticsByUUIDQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });

  return result;
};

const useGetCurrentDriftQueryWithPolling = () => {
  const { uuid } = useParams();

  const { modalPayload: { data: modalData } } = useModals();

  const { data: model } = useGetModelByUUIDQuery({ uuid }, { skip: modalData?.uuid });
  const latestCurrentUuid = model?.latestCurrentUuid;

  const currentUUID = modalData?.uuid !== undefined ? modalData.uuid : latestCurrentUuid;

  const result = useGetCurrentDriftQuery({ uuid, currentUUID }, { skip: !currentUUID });
  const status = result.data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentDriftQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });

  return result;
};

export {
  useGetCurrentDataQualityQueryWithPolling,
  useGetCurrentDriftQueryWithPolling,
  useGetCurrentImportsQueryWithPolling,
  useGetCurrentModelQualityQueryWithPolling,
  useGetCurrentStatisticsQueryWithPolling,
  useGetReferenceDataQualityQueryWithPolling,
  useGetReferenceImportsQueryWithPolling,
  useGetReferenceModelQualityQueryWithPolling,
  useGetReferenceStatisticsQueryWithPolling,
};
