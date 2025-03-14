import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useFormbitContext } from '@radicalbit/formbit';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';

const { useAddNewProjectMutation } = tracingApiSlice;

export default () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const { isDirty, isFormInvalid, submitForm } = useFormbitContext();

  const [triggerAddNewProject, args] = useAddNewProjectMutation();

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnSubmit = () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { name } }, setError) => {
      const response = await triggerAddNewProject({ name });

      if (response.error) {
        console.error(response.error);
        setError('silent.backed', response.error);
        return;
      }

      searchParams.delete('modal');

      navigate({ pathname: `projects/${response.data.uuid}`, search: searchParams.toString() });
    });
  };

  return { handleOnSubmit, args, isSubmitDisabled };
};
