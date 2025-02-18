/* import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { useFormbitContext } from '@radicalbit/formbit'; */
import { useFormbitContext } from '@radicalbit/formbit';
import { useGetCompletionModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';

export default () => {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const tokens = data?.modelQuality?.tokens ?? [];

  const meanPerPhrase = data?.modelQuality?.meanPerPhrase ?? [];

  const { form: { __metadata: { searchToken } } } = useFormbitContext();

  if (!data) {
    return [];
  }

  const filteredTokens = tokens.filter(({ messageContent }) => messageContent.toLowerCase().includes(searchToken.toLowerCase()));

  return { tokens: filteredTokens, meanPerPhrase };
};
