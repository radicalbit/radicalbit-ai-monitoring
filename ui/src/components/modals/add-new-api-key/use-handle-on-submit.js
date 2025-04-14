import useModals from '@Hooks/use-modals';
import { tracingApiSlice } from '@State/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { useSearchParams } from 'react-router-dom';

const { useAddNewApiKeyMutation, useAddNewProjectMutation } = tracingApiSlice;

export default () => {
  const [searchParams] = useSearchParams();
  const { hideModal } = useModals();

  const { isDirty, isFormInvalid, submitForm } = useFormbitContext();

  const [triggerAddNewApiKey, args] = useAddNewApiKeyMutation({ fixedCacheKey: 'add-new-api-key' });
  const [, addNewProjectArgs] = useAddNewProjectMutation({ fixedCacheKey: 'add-new-project' });

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnSubmit = (projectUuid) => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { name } }, setError) => {
      const response = await triggerAddNewApiKey({ projectUuid, data: { name } });

      if (response.error) {
        console.error(response.error);
        setError('silent.backed', response.error);
        return;
      }
      addNewProjectArgs.reset();
      searchParams.delete('modal');
      hideModal();
    });
  };

  return {
    handleOnSubmit, args, isSubmitDisabled,
  };
};
