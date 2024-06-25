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

const useGetReferenceDataQualityQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const status = data?.jobStatus;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceDataQualityQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });
};

const useGetReferenceModelQualityQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetReferenceModelQualityQuery({ uuid });
  const status = data?.jobStatus;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceModelQualityQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });
};

const useGetReferenceStatisticsQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetReferenceStatisticsQuery({ uuid });
  const status = data?.jobStatus;
  const isReferenceImporting = status === JOB_STATUS.IMPORTING;

  useGetReferenceStatisticsQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isReferenceImporting });
};

const useGetCurrentImportsQueryWithPolling = () => {
  const { uuid } = useParams();
  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.CURRENT_IMPORT));

  const { data } = useGetCurrentImportsQuery({ uuid, queryParams });
  const currentActiveImport = data?.items.filter((i) => i.status === JOB_STATUS.IMPORTING).length ?? 0;

  useGetCurrentImportsQuery({ uuid, queryParams }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: currentActiveImport === 0 });
};

const useGetCurrentDataQualityQueryWithPolling = () => {
  const { modalPayload: { data: modalData } } = useModals();
  const isModal = modalData?.uuid !== undefined;

  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const currentUUID = model?.latestCurrentUUID;

  const { data } = useGetCurrentDataQualityQuery({ uuid, currentUUID }, { skip: isModal });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentDataQualityQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentModelQualityQueryWithPolling = () => {
  const { modalPayload: { data: modalData } } = useModals();
  const isModal = modalData?.uuid !== undefined;

  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const currentUUID = model?.latestCurrentUUID;

  const { data } = useGetCurrentModelQualityQuery({ uuid, currentUUID }, { skip: isModal });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentModelQualityQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentStatisticsQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const currentUUID = model?.latestCurrentUUID;

  const { data } = useGetCurrentStatisticsByUUIDQuery({ uuid, currentUUID });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentStatisticsByUUIDQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentDriftQueryWithPolling = () => {
  const { modalPayload: { data: modalData } } = useModals();
  const isModal = modalData?.uuid !== undefined;

  const { uuid } = useParams();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const currentUUID = model?.latestCurrentUUID;

  const { data } = useGetCurrentDriftQuery({ uuid, currentUUID }, { skip: isModal });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentDriftQuery({ uuid, currentUUID }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
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
