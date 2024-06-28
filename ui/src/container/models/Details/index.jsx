import { ModelTypeEnum } from '@Src/store/state/models/constants';
import { modelsApiSlice } from '@State/models/api';
import { useParams } from 'react-router-dom';
import BinaryClassificationMetrics from './binary-classification';
import MultiClassificationMetrics from './multi-classification';

const { useGetModelByUUIDQuery } = modelsApiSlice;

export function ModelDetails() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const modelType = data?.modelType;

  switch (modelType) {
    case ModelTypeEnum.BINARY_CLASSIFICATION:
      return <BinaryClassificationMetrics />;

    case ModelTypeEnum.MULTI_CLASSIFICATION:
      return <MultiClassificationMetrics />;

    default:
      return false;
  }
}
