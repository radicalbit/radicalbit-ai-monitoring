import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { actions as contextConfigurationActions } from '@State/context-configuration';
import { useDispatch } from 'react-redux';
import { qsEncode64JSON } from '@Helpers/queryParams';

const { setRawConfiguration } = contextConfigurationActions;

const useContextConfigurationFromUrlEffect = () => {
  const { search } = useLocation();
  const dispatch = useDispatch();

  useEffect(() => {
    const override = qsEncode64JSON(search, 'configuration');

    dispatch(setRawConfiguration({ override }));
  }, [dispatch, search]);
};

export { useContextConfigurationFromUrlEffect };
