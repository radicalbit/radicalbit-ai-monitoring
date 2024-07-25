export default () => {
  const args = { isLoading: false };

  const handleOnSubmit = () => {
    console.debug('test');
  };

  return [handleOnSubmit, args];
};
