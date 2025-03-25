import * as yup from 'yup';

const schema = yup.object().shape({
  fromTimestamp: yup.string()
    .test('is-before', 'From timestamp must be earlier than To timestamp', (value, { parent }) => {
      const { toTimestamp } = parent;

      return value && toTimestamp ? new Date(value) < new Date(toTimestamp) : true;
    }).required('From timestamp is required'),

  toTimestamp: yup.string().required('To timestamp is required'),
});

export default schema;
