import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { useGetCurrentDriftQueryWithPolling } from '@State/models/polling-hook';
import { useFormbitContext } from '@radicalbit/formbit';

export default () => {
  const { data } = useGetCurrentDriftQueryWithPolling();
  const items = data?.drift?.featureMetrics ?? [];

  const { form: { __metadata: { isNumericalSelected, isCategoricalSelected, selectedFeatures } } } = useFormbitContext();

  if (!data) {
    return [];
  }

  if (!isNumericalSelected && !isCategoricalSelected) {
    return [];
  }

  return selectedFeatures?.length > 0
    ? items.filter(({ featureName, fieldType }) => {
      const isSelected = selectedFeatures.includes(featureName);
      const isNumerical = isNumericalSelected && fieldType === FEATURE_TYPE.NUMERICAL;
      const isCategorical = isCategoricalSelected && fieldType === FEATURE_TYPE.CATEGORICAL;

      return isSelected && (isNumerical || isCategorical);
    })
    : items.filter(({ fieldType }) => {
      const isNumerical = isNumericalSelected && fieldType === FEATURE_TYPE.NUMERICAL;
      const isCategorical = isCategoricalSelected && fieldType === FEATURE_TYPE.CATEGORICAL;

      return isNumerical || isCategorical;
    });
};
