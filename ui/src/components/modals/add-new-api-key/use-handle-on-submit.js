import useModals from '@Hooks/use-modals';
import { tracingApiSlice } from '@State/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { useSearchParams } from 'react-router-dom';

const { useAddNewApiKeyMutation, useAddNewProjectMutation } = tracingApiSlice;

export default () => {
  const { modalPayload: { data: { uuid } } } = useModals();

  const [searchParams] = useSearchParams();
  const { hideModal } = useModals();

  const { isDirty, isFormInvalid, submitForm } = useFormbitContext();

  const [triggerAddNewApiKey, args] = useAddNewApiKeyMutation({ fixedCacheKey: 'add-new-api-key' });
  const [, addNewProjectArgs] = useAddNewProjectMutation({ fixedCacheKey: 'add-new-project' });

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnSubmit = () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { name } }, setError) => {
      const response = await triggerAddNewApiKey({ uuid, data: { name } });

      if (response.error) {
        setError('silent.backend', response.error.message || response.error.data.message || 'Something went wrong');
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
