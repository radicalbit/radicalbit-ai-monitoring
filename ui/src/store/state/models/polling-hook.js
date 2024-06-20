import { DEFAULT_POLLING_INTERVAL, JOB_STATUS, NamespaceEnum } from '@Src/constants';
import { API_TAGS } from '@Src/store/apis';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
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
  const [pollingInterval, setPollingInterval] = useState(0);
  const dispatch = useDispatch();
  const { uuid } = useParams();
  const { data } = useGetReferenceImportsQuery({ uuid }, { pollingInterval });
  const status = data?.items[0]?.status;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
        dispatch(modelsApiSlice.util.invalidateTags([{ type: API_TAGS.REFERENCE_IMPORT, id: uuid }]));
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval, dispatch, uuid]);
};

const useGetReferenceDataQualityQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetReferenceDataQualityQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

const useGetReferenceModelQualityQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetReferenceModelQualityQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

const useGetReferenceStatisticsQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetReferenceStatisticsQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

const useGetCurrentImportsQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const dispatch = useDispatch();

  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.CURRENT_IMPORT));

  const { uuid } = useParams();
  const { data } = useGetCurrentImportsQuery({ uuid, queryParams }, { pollingInterval });
  const isCurrentImporting = data?.items.filter((i) => i.status === JOB_STATUS.IMPORTING).length > 0;

  useEffect(() => {
    if (isCurrentImporting && pollingInterval === 0) {
      setPollingInterval(DEFAULT_POLLING_INTERVAL);
      dispatch(modelsApiSlice.util.invalidateTags([{ type: API_TAGS.CURRENT_IMPORT, id: uuid }]));
    }
    if (!isCurrentImporting) {
      setPollingInterval(0);
    }
  }, [isCurrentImporting, pollingInterval, setPollingInterval, dispatch, uuid]);
};

const useGetCurrentDataQualityLatestQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetCurrentDataQualityLatestQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

const useGetCurrentModelQualityLatestQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetCurrentModelQualityLatestQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

const useGetCurrentStatisticsLatestQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetCurrentStatisticsLatestQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

const useGetCurrentDriftLatestQueryWithPolling = () => {
  const [pollingInterval, setPollingInterval] = useState(0);
  const { uuid } = useParams();
  const { data } = useGetCurrentDriftLatestQuery({ uuid }, { pollingInterval });
  const status = data?.jobStatus;

  useEffect(() => {
    if (status) {
      if (status === JOB_STATUS.IMPORTING && pollingInterval === 0) {
        setPollingInterval(DEFAULT_POLLING_INTERVAL);
      }
      if (status !== JOB_STATUS.IMPORTING) {
        setPollingInterval(0);
      }
    }
  }, [status, pollingInterval, setPollingInterval]);
};

export {
  useGetCurrentDataQualityLatestQueryWithPolling, useGetCurrentImportsQueryWithPolling, useGetCurrentModelQualityLatestQueryWithPolling,
  useGetCurrentStatisticsLatestQueryWithPolling, useGetReferenceDataQualityQueryWithPolling, useGetReferenceImportsQueryWithPolling, useGetReferenceModelQualityQueryWithPolling,
  useGetReferenceStatisticsQueryWithPolling, useGetCurrentDriftLatestQueryWithPolling,
};
