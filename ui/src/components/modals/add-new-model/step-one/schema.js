import { DataTypeEnum, GranularityEnum, ModelTypeEnum } from '@State/models/constants';
import * as yup from 'yup';

const schema = yup.object({
  name: yup.string()
    .max(25, 'Name max length is 25 characters')
    .matches(/^[A-Za-z0-9_\\-]+$/, 'Name can be filled only with letters, numbers, underscores and dashes')
    .matches(/^[A-Za-z]/, 'Name must start with a letter')
    .required(),

  modelType: yup.string()
    .oneOf(Object.values(ModelTypeEnum))
    .required('Model type is required'),

  dataType: yup.string()
    .oneOf(Object.values(DataTypeEnum))
    .required('Data type is required'),

  granularity: yup.string()
    .oneOf(Object.values(GranularityEnum))
    .required('Granularity is required'),

  framework: yup.string(),

  algorithm: yup.string(),

});

export default schema;
