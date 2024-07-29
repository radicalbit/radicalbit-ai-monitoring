import * as yup from 'yup';

const schema = yup.object().shape({
  variables: yup.mixed(),
});

export default schema;
