import { DETAIL_LAYOUT_DARK_MODE_CONFIGURATION, DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import useSetDarkMode from '@Hooks/use-set-dark-mode';
import { modelsApiSlice } from '@State/models/api';
import { ModelTypeEnum } from '@State/models/constants';
import { useParams } from 'react-router-dom';
import BinaryClassificationMetrics from './binary-classification';
import MultiClassificationMetrics from './multi-classification';
import RegressionMetrics from './regression';

const { useGetModelByUUIDQuery } = modelsApiSlice;

export function ModelDetails() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  useSetDarkMode(DETAIL_LAYOUT_DARK_MODE_CONFIGURATION, DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION);

  const modelType = data?.modelType;

  switch (modelType) {
    case ModelTypeEnum.REGRESSION:
      return <RegressionMetrics />;

    case ModelTypeEnum.BINARY_CLASSIFICATION:
      return <BinaryClassificationMetrics />;

    case ModelTypeEnum.MULTI_CLASSIFICATION:
      return <MultiClassificationMetrics />;

    default:
      return false;
  }
}
