import featureFlags from './feature-flag.json';

const getIsProjectTracingEnabled = () => {
  const isProjectTracingEnabled = featureFlags['project-tracing-enabled'];

  return isProjectTracingEnabled;
};

export default getIsProjectTracingEnabled;
