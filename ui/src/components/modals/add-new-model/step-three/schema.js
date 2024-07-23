import * as yup from 'yup';

const schemaFeatureOutput = yup.object().shape({
  outputKeys: yup.array().of(yup.string()).min(3, 'Select at least one target, one prediction and one timestamp').required(),
  featureKeys: yup.array().of(yup.string()),
});

export default schemaFeatureOutput;
