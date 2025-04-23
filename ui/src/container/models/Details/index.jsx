import { useInitDarkMode } from '@Components/dark-mode/hooks';
import { DETAIL_LAYOUT_DARK_MODE_CONFIGURATION, DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import { modelsApiSlice } from '@State/models/api';
import { ModelTypeEnum } from '@State/models/constants';
import { useParams } from 'react-router-dom';
import BinaryClassificationMetrics from './binary-classification';
import MultiClassificationMetrics from './multi-classification';
import RegressionMetrics from './regression';
import TextGenerationMetrics from './text-generation';
import EmbeddingsMetrics from './embeddings';

const { useGetModelByUUIDQuery } = modelsApiSlice;

export function ModelDetails() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  useInitDarkMode(DETAIL_LAYOUT_DARK_MODE_CONFIGURATION, DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION);

  const modelType = data?.modelType;

  switch (modelType) {
    case ModelTypeEnum.REGRESSION:
      return <RegressionMetrics />;

    case ModelTypeEnum.BINARY_CLASSIFICATION:
      return <BinaryClassificationMetrics />;

    case ModelTypeEnum.MULTI_CLASSIFICATION:
      return <MultiClassificationMetrics />;

    case ModelTypeEnum.TEXT_GENERATION:
      return <TextGenerationMetrics />;

    case ModelTypeEnum.EMBEDDINGS:
      return <EmbeddingsMetrics />;

    default:
      return false;
  }
}
