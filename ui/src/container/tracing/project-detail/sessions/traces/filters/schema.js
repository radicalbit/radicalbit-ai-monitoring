import * as yup from 'yup';

const schema = yup.object().shape({
  sessionUuid: yup.string().nullable(),
  fromTimestamp: yup.string().nullable(),
  toTimestamp: yup.string().nullable(),
});

export default schema;
