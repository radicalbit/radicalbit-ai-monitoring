import { useFormbitContext } from '@radicalbit/formbit';
import { modelsApiSlice } from '@State/models/api';
import { useParams } from 'react-router';

const { useUpdateModelFeaturesMutation } = modelsApiSlice;

export default () => {
  const { uuid } = useParams();
  const { isDirty, submitForm } = useFormbitContext();

  const [trigger, args] = useUpdateModelFeaturesMutation();

  const isSubmitDisabled = !isDirty;

  const handleOnSubmit = async () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { variables } }, setError, clearIsDirty) => {
      const filteredVariables = variables.filter(({ rowType }) => rowType === '');

      const response = await trigger({ data: { features: filteredVariables }, uuid, successMessage: 'Model updated' });

      if (response.error) {
        console.error(response.error);
        setError('silent.backed', response.error);
        return;
      }

      clearIsDirty();
    });
  };

  return [handleOnSubmit, args, isSubmitDisabled];
};
