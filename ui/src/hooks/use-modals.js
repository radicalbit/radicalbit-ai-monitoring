import { useNavigate } from 'react-router';
import qs from 'query-string';
import { useCallback } from 'react';
import { ModalsEnum } from '@Src/constants';
import { decode, encode } from '@Src/helpers/base-64';

const handleQueryString = (search, key, value) => {
  const queryString = qs.parse(search);

  if (value) {
    queryString[key] = value;
  } else if (queryString[key]) {
    delete queryString[key];
  }

  return qs.stringify(queryString);
};

export const getModal = (search) => {
  const { modal } = qs.parse(search);

  return (modal && typeof modal === 'string')
    ? JSON.parse(decode(modal))
    : {};
};

export default () => {
  const navigate = useNavigate();

  const showModal = useCallback((modalName, data = {}) => {
    const parsedSearch = handleQueryString(
      window.location.search,
      ModalsEnum.QUERY_NAME,
      encode({ modalName, data }),
    );

    navigate(`?${parsedSearch}`);
  }, [navigate]);

  const hideModal = useCallback(({ qpToDelete = [] } = {}) => {
    const params = new URLSearchParams(window.location.search);

    params.delete(ModalsEnum.QUERY_NAME);
    qpToDelete.forEach((qp) => params.delete(qp));

    navigate(`?${params.toString()}`);
  }, [navigate]);

  const modalPayload = getModal(window.location.search);

  return { showModal, hideModal, modalPayload };
};
