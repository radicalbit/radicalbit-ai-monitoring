import * as yup from 'yup';

const schemaCsv = yup.object().shape({
  file: yup
    .mixed()
    .required('CSV File is required'),

  separator: yup.string()
    .oneOf([',', ';'])
    .required('Please insert a separator'),
});

export default schemaCsv;
