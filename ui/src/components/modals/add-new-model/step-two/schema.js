import * as yup from 'yup';

const schemaCsv = yup.object().shape({
  file: yup
    .mixed()
    .required('CSV File is required'),
});

export default schemaCsv;
