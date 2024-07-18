import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { useGetCurrentDataQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { useFormbitContext } from '@radicalbit/formbit';
import { useParams } from 'react-router';

const { useGetReferenceDataQualityQuery } = modelsApiSlice;

export default () => {
  const { uuid } = useParams();

  const { data: currentData } = useGetCurrentDataQualityQueryWithPolling();
  const items = currentData?.dataQuality?.featureMetrics ?? [];

  const { data: referenceData } = useGetReferenceDataQualityQuery({ uuid });
  const referenceItems = referenceData?.dataQuality?.featureMetrics ?? [];

  const { form: { __metadata: { isNumericalSelected, isCategoricalSelected, selectedFeatures } } } = useFormbitContext();

  if (!currentData) {
    return [];
  }

  if (!isNumericalSelected && !isCategoricalSelected) {
    return [];
  }

  const filteredFeatures = selectedFeatures?.length > 0
    ? items.filter(({ featureName, type }) => {
      const isSelected = selectedFeatures.includes(featureName);
      const isNumerical = isNumericalSelected && type === FEATURE_TYPE.NUMERICAL;
      const isCategorical = isCategoricalSelected && type === FEATURE_TYPE.CATEGORICAL;

      return isSelected && (isNumerical || isCategorical);
    })
    : items.filter(({ type }) => {
      const isNumerical = isNumericalSelected && type === FEATURE_TYPE.NUMERICAL;
      const isCategorical = isCategoricalSelected && type === FEATURE_TYPE.CATEGORICAL;

      return isNumerical || isCategorical;
    });

  return filteredFeatures.map((feature) => {
    if (feature.type === FEATURE_TYPE.CATEGORICAL) {
      const referenceCategoryFrequency = referenceItems?.find((r) => r.type === FEATURE_TYPE.CATEGORICAL && r.featureName === feature.featureName)?.categoryFrequency;
      const categoryFrequencyUpdated = feature.categoryFrequency.map((m) => {
        const rFounded = referenceCategoryFrequency.find((r) => r.name === m.name);

        return {
          ...m,
          frequency: Math.floor(m.frequency * 100),
          referenceCount: rFounded?.count,
          referenceFrequency: (rFounded?.frequency) ? Math.floor(rFounded.frequency * 100) : 0,
        };
      });

      return {
        ...feature,
        categoryFrequency: categoryFrequencyUpdated,
      };
    }

    return feature;
  });
};
