import { useFormbitContext } from '@radicalbit/formbit';
import { modelsApiSlice } from '@State/models/api';
import { useParams } from 'react-router';

const { useEditModelMutation, useGetModelByUUIDQuery } = modelsApiSlice;

export default () => {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const { isDirty, submitForm } = useFormbitContext();

  const [triggerEditModel, args] = useEditModelMutation();

  const isSubmitDisabled = !isDirty;

  const handleOnSubmit = async () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { variables } }, setError, clearIsDirty) => {
      const filteredVariables = variables.filter(({ rowType }) => rowType === '');

      const updatedData = {
        ...data,
        features: filteredVariables,
      };

      const response = await triggerEditModel({ data: updatedData, successMessage: 'Model updated' });

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
