import * as yup from 'yup';

const schema = yup.object({
  editedName: yup.string()
    .max(25, 'Name max length is 25 characters')
    .matches(/^[A-Za-z0-9_\\-]+$/, 'Name can be filled only with letters, numbers, underscores and dashes')
    .matches(/^[A-Za-z]/, 'Name must start with a letter')
    .required(),

});

export default schema;
