import * as yup from 'yup';

const schemaCsv = yup.object().shape({
  target: yup.object().required('Please select the target'),

  prediction: yup.object().required('Please select the prediction'),

  timestamp: yup.object().required('Please select the timestamp'),
});

export default schemaCsv;
