import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { useFormbitContext } from '@radicalbit/formbit';
import { useParams } from 'react-router-dom';
import { modelsApiSlice } from '@State/models/api';

const { useGetReferenceDataQualityQuery } = modelsApiSlice;

export default () => {
  const { uuid } = useParams();

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const items = data?.dataQuality?.featureMetrics ?? [];

  const { form: { __metadata: { isNumericalSelected, isCategoricalSelected, selectedFeatures } } } = useFormbitContext();

  if (!data) {
    return [];
  }

  if (!isNumericalSelected && !isCategoricalSelected) {
    return [];
  }

  return selectedFeatures?.length > 0
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
};
