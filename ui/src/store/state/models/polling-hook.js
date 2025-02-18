import useModals from '@Hooks/use-modals';
import { DEFAULT_POLLING_INTERVAL, JOB_STATUS, NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import { modelsApiSlice } from './api';

const { selectQueryParamsSelector } = contextConfigurationSelectors;

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
  useGetModelsQuery,
  useGetOverallModelListQuery,
  useGetCompletionModelQualityQuery,
  useGetCompletionImportsQuery,
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

  const result = useGetCurrentStatisticsByUUIDQuery({ uuid, currentUUID }, { skip: !currentUUID });
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

const useGetModelsQueryWithPolling = () => {
  const queryParams = useSelector((state) => selectQueryParamsSelector(state, NamespaceEnum.MODELS));
  const result = useGetModelsQuery({ queryParams });

  const isReferencePending = result.data?.items.some((d) => d.latestReferenceJobStatus === JOB_STATUS.IMPORTING);
  const isCurrentPending = result.data?.items.some((d) => d.latestCurrentJobStatus === JOB_STATUS.IMPORTING);
  const isCompletionPending = result.data?.items.some((d) => d.latestCompletionJobStatus === JOB_STATUS.IMPORTING);
  const isPending = isReferencePending || isCurrentPending || isCompletionPending;

  useGetModelsQuery({ queryParams }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isPending });

  return result;
};

const useGetOverallModelListQueryWithPolling = () => {
  const result = useGetOverallModelListQuery({ limit: 10 });

  const isReferencePending = result.data?.some((d) => d.latestReferenceJobStatus === JOB_STATUS.IMPORTING);
  const isCurrentPending = result.data?.some((d) => d.latestCurrentJobStatus === JOB_STATUS.IMPORTING);
  const isPending = isReferencePending || isCurrentPending;

  useGetOverallModelListQuery({ limit: 10 }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isPending });
  return result;
};

const useGetCompletionModelQualityQueryWithPolling = () => {
  const { uuid } = useParams();
  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const latestCompletionUuid = model?.latestCompletionUuid;

  const result = useGetCompletionModelQualityQuery({ uuid, latestCompletionUuid }, { skip: !latestCompletionUuid });
  const status = result.data?.jobStatus;
  const isCompletionImporting = status === JOB_STATUS.IMPORTING;

  useGetCompletionModelQualityQuery({ uuid, latestCompletionUuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCompletionImporting });

  return result;
};

const useGetCompletionImportsQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetCompletionImportsQuery({ uuid });
  const status = data?.items[0]?.status;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetCompletionImportsQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });
};

export {
  useGetCurrentDataQualityQueryWithPolling,
  useGetCurrentDriftQueryWithPolling,
  useGetCurrentImportsQueryWithPolling,
  useGetCurrentModelQualityQueryWithPolling,
  useGetCurrentStatisticsQueryWithPolling, useGetModelsQueryWithPolling,
  useGetOverallModelListQueryWithPolling, useGetReferenceDataQualityQueryWithPolling,
  useGetReferenceImportsQueryWithPolling,
  useGetReferenceModelQualityQueryWithPolling,
  useGetReferenceStatisticsQueryWithPolling,
  useGetCompletionModelQualityQueryWithPolling,
  useGetCompletionImportsQueryWithPolling,
};
