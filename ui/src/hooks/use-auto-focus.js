import { useEffect } from 'react';

export default (ref) => {
  useEffect(() => {
    ref.current?.focus();
  }, [ref]);
};
