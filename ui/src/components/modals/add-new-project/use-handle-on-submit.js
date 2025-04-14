import { TRACING_TABS_ENUM } from '@Container/tracing/constants';
import { tracingApiSlice } from '@State/tracing/api';

import { useFormbitContext } from '@radicalbit/formbit';
import { useNavigate, useSearchParams } from 'react-router-dom';

const { useAddNewProjectMutation } = tracingApiSlice;

export default () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const { isDirty, isFormInvalid, submitForm } = useFormbitContext();

  const [triggerAddNewProject, args] = useAddNewProjectMutation({ fixedCacheKey: 'add-new-project' });

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

      navigate({ pathname: `projects/${response.data.uuid}`, search: `tab=${TRACING_TABS_ENUM.SETTINGS}` });
    });
  };

  return { handleOnSubmit, args, isSubmitDisabled };
};
