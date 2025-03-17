import { useFormbitContext } from '@radicalbit/formbit';
import { useGetCompletionModelQualityQueryWithPolling } from '@State/models/polling-hook';

export default () => {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const tokens = data?.modelQuality?.tokens ?? [];

  const meanPerPhrase = data?.modelQuality?.meanPerPhrase ?? [];

  const { form } = useFormbitContext();
  const metadata = form?.__metadata;

  if (!data) {
    return [];
  }

  const filteredTokens = getFilteredTokens({ tokens, metadata });

  return { tokens: filteredTokens, meanPerPhrase };
};

const getFilteredTokens = ({ tokens, metadata }) => {
  const searchToken = metadata?.searchToken;
  const isSearchForModelName = metadata?.isSearchForModelName;
  const isSearchForTimestamp = metadata?.isSearchForTimestamp;

  if (!isSearchForModelName && !isSearchForTimestamp) {
    return tokens.filter(({ messageContent }) => messageContent.toLowerCase().includes(searchToken.toLowerCase()));
  }

  if (isSearchForModelName && isSearchForTimestamp) {
    return tokens.filter(({ messageContent }) => messageContent.toLowerCase().includes(searchToken.toLowerCase()));
  }

  if (isSearchForModelName) {
    return tokens.filter(({ modelName }) => modelName.toLowerCase().includes(searchToken.toLowerCase()));
  }

  if (isSearchForTimestamp) {
    return tokens.filter(({ rbitTimestamp }) => rbitTimestamp.toLowerCase().includes(searchToken.toLowerCase()));
  }

  return tokens;
};
