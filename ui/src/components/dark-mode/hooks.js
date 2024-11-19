import { useCallback, useEffect } from 'react';
import { useDispatch } from 'react-redux';

const useInitDarkMode = (darkActions = [], lightActions = []) => {
  const dispatch = useDispatch();

  useEffect(() => {
    const isDarkMode = window.localStorage.getItem('enable-dark-mode');

    if (isDarkMode) {
      window.document.body.classList.add('dark');
    } else {
      window.document.body.classList.remove('dark');
    }

    if (isDarkMode) {
      darkActions.forEach((action) => dispatch(action()));
    } else {
      lightActions.forEach((action) => dispatch(action()));
    }
  }, [darkActions, dispatch, lightActions]);
};

const useSetDarkMode = (darkActions = [], lightActions = []) => {
  const dispatch = useDispatch();

  const enableDarkMode = useCallback(() => {
    window.localStorage.setItem('enable-dark-mode', true);
    window.document.body.classList.add('dark');

    darkActions.forEach((action) => dispatch(action()));
  }, [darkActions, dispatch]);

  const enableLightMode = useCallback(() => {
    window.localStorage.removeItem('enable-dark-mode');
    window.document.body.classList.remove('dark');

    lightActions.forEach((action) => dispatch(action()));
  }, [dispatch, lightActions]);

  return { enableDarkMode, enableLightMode };
};

const useIsDarkMode = () => window.document.body.classList.contains('dark');

export { useInitDarkMode, useIsDarkMode, useSetDarkMode };
