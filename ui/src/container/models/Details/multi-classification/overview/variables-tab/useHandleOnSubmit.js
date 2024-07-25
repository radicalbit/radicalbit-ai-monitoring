import { useFormbitContext } from '@radicalbit/formbit';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { useParams } from 'react-router';

const { useEditModelMutation, useGetModelByUUIDQuery } = modelsApiSlice;

export default () => {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const { resetForm, setError, form } = useFormbitContext();

  const [triggerEditModel, args] = useEditModelMutation();

  const handleOnSubmit = async () => {
    if (args.isLoading) {
      return;
    }
    const variables = form?.__metadata.variables ?? [];
    const filteredVariables = variables.filter(({ rowType }) => rowType === '');

    const updatedData = {
      ...data,
      features: filteredVariables,
    };

    const response = await triggerEditModel({ data: updatedData });

    if (response.error) {
      console.error(response.error);
      setError('silent.backed', response.error);
      return;
    }

    resetForm();
  };

  return [handleOnSubmit, args];
};
