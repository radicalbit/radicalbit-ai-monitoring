import { DRIFT_TEST_ENUM } from '@Src/constants';
import { useGetCurrentDriftQueryWithPolling } from '@Src/store/state/models/polling-hook';
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
    ? items.filter(({ featureName, driftCalc: { type } }) => {
      const isSelected = selectedFeatures.includes(featureName);
      const isNumerical = isNumericalSelected && type === DRIFT_TEST_ENUM.CHI2;
      const isCategorical = isCategoricalSelected && type === DRIFT_TEST_ENUM.KS;

      return isSelected && (isNumerical || isCategorical);
    })
    : items.filter(({ driftCalc: { type } }) => {
      const isNumerical = isNumericalSelected && type === DRIFT_TEST_ENUM.CHI2;
      const isCategorical = isCategoricalSelected && type === DRIFT_TEST_ENUM.KS;

      return isNumerical || isCategorical;
    });
};
