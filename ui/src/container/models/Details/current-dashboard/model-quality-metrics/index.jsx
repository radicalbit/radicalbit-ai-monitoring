import { modelsApiSlice } from '@Src/store/state/models/api';
import { ModelTypeEnum } from '@State/models/constants';
import { memo } from 'react';
import { useParams } from 'react-router';
import BinaryClassificationMetrics from './binary-classification-metrics';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function ModelQualityMetrics() {
  const { uuid } = useParams();

  const { data } = useGetModelByUUIDQuery({ uuid });
  const modelType = data?.modelType;

  switch (modelType) {
    case ModelTypeEnum.BINARY_CLASSIFICATION:
      return <BinaryClassificationMetrics />;

    default:
      return false;
  }
}

export default memo(ModelQualityMetrics);
