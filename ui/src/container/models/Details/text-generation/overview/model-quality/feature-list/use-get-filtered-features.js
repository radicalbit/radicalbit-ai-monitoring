/* import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { useFormbitContext } from '@radicalbit/formbit'; */
import { useGetCompletionModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';

export default () => {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const tokens = data?.modelQuality?.tokens ?? [];
  const meanPerPhrase = data?.modelQuality?.meanPerPhrase ?? [];

  // const { form: { __metadata: { isNumericalSelected, isCategoricalSelected, selectedFeatures } } } = useFormbitContext();

  if (!data) {
    return [];
  }

  /*   if (!isNumericalSelected && !isCategoricalSelected) {
    return [];
  } */

  return { tokens, meanPerPhrase };
};
