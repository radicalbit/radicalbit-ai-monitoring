import { DEFAULT_POLLING_INTERVAL, JOB_STATUS, NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import { modelsApiSlice } from './api';

const {
  useGetReferenceImportsQuery,
  useGetReferenceDataQualityQuery,
  useGetReferenceModelQualityQuery,
  useGetReferenceStatisticsQuery,
  useGetCurrentImportsQuery,
  useGetCurrentDataQualityLatestQuery,
  useGetCurrentModelQualityLatestQuery,
  useGetCurrentStatisticsLatestQuery,
  useGetCurrentDriftLatestQuery,
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
  const isCurrentImporting = data?.items.filter((i) => i.status === JOB_STATUS.IMPORTING).length > 0;

  useGetCurrentImportsQuery({ uuid, queryParams }, { DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentDataQualityLatestQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetCurrentDataQualityLatestQuery({ uuid });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentDataQualityLatestQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentModelQualityLatestQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetCurrentModelQualityLatestQuery({ uuid });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentModelQualityLatestQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentStatisticsLatestQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetCurrentStatisticsLatestQuery({ uuid });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentStatisticsLatestQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

const useGetCurrentDriftLatestQueryWithPolling = () => {
  const { uuid } = useParams();

  const { data } = useGetCurrentDriftLatestQuery({ uuid });
  const status = data?.jobStatus;
  const isCurrentImporting = status === JOB_STATUS.IMPORTING;

  useGetCurrentDriftLatestQuery({ uuid }, { pollingInterval: DEFAULT_POLLING_INTERVAL, skip: !isCurrentImporting });
};

export {
  useGetCurrentDataQualityLatestQueryWithPolling, useGetCurrentDriftLatestQueryWithPolling, useGetCurrentImportsQueryWithPolling, useGetCurrentModelQualityLatestQueryWithPolling,
  useGetCurrentStatisticsLatestQueryWithPolling, useGetReferenceDataQualityQueryWithPolling, useGetReferenceImportsQueryWithPolling, useGetReferenceModelQualityQueryWithPolling,
  useGetReferenceStatisticsQueryWithPolling,
};
