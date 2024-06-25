const qs = (param) => new URLSearchParams(window.location.search).get(param);

const qsContextConfiguration = () => {
  const value = qs('configuration');

  return value ? `configuration=${value}` : '';
};

const qsSetEncode64JSON = (param, json) => {
  const encode64 = btoa(JSON.stringify(json));
  const newQS = new URLSearchParams(window.location.search);
  newQS.set(param, encode64);

  return newQS.toString();
};

const qsEncode64JSON = (search, param) => {
  const qsParam = new URLSearchParams(search).get(param);
  const qsAtob = atob(qsParam ?? '');

  if (qsParam === null) {
    return {};
  }

  try {
    return JSON.parse(qsAtob);
  } catch (e) {
    console.warn('Error in parsing qsEncode64JSON: ', e);
    return {};
  }
};

export default qs;

export {
  qsContextConfiguration,
  qsEncode64JSON,
  qsSetEncode64JSON,
};
