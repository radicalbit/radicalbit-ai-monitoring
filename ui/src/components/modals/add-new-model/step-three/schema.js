import * as yup from 'yup';

const schemaFeatureOutput = yup.object().shape({
  outputKeys: yup.array().of(yup.string()).min(1, 'Select at least one output').required(),
  featureKeys: yup.array().of(yup.string()).min(1, 'Select at least one feture').required(),
});

export default schemaFeatureOutput;
