import useModals from '@Hooks/use-modals';
import { tracingApiSlice } from '@State/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { useSearchParams } from 'react-router-dom';

const { useEditTracingProjectMutation } = tracingApiSlice;

export default () => {
  const { modalPayload: { data: { uuid } } } = useModals();
  const [searchParams] = useSearchParams();

  const { isDirty, isFormInvalid, submitForm } = useFormbitContext();

  const [triggerEditProject, args] = useEditTracingProjectMutation({ fixedCacheKey: `edit-new-project-${uuid}` });

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnSubmit = () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { name } }, setError) => {
      const response = await triggerEditProject({ uuid, name });

      if (response.error) {
        setError('silent.backend', response.error.message || response.error.data.message || 'Something went wrong');
        return;
      }

      searchParams.delete('modal');
    });
  };

  return { handleOnSubmit, args, isSubmitDisabled };
};
