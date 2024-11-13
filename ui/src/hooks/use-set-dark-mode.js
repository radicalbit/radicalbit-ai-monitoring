import { useEffect } from 'react';
import { useDispatch } from 'react-redux';

const useSetDarkMode = (darkActions = [], lightActions = []) => {
  const dispatch = useDispatch();

  useEffect(() => {
    const isDarkMode = window.localStorage.getItem('enable-dark-mode');

    if (isDarkMode) {
      darkActions.forEach((action) => dispatch(action()));
    } else {
      lightActions.forEach((action) => dispatch(action()));
    }
  }, [darkActions, dispatch, lightActions]);
};

export default useSetDarkMode;
