import { globalConfigSliceActions } from '@State/global-configuration/slice';
import { modelsApiSlice } from '@State/models/api';
import { useDispatch } from 'react-redux';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { DataTypeEnum } from '@State/models/constants';
import { useModalContext } from '../modal-context-provider';

const { useAddNewModelMutation } = modelsApiSlice;

export default () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const dispatch = useDispatch();

  const { useFormbit, useFormbitStepOne } = useModalContext();

  const { isDirty, isFormInvalid, submitForm } = useFormbit;
  const { form: formStepOne } = useFormbitStepOne;

  const [triggerAddNewModel, args] = useAddNewModelMutation();

  const isSubmitDisabled = !isDirty || isFormInvalid() || args.isLoading;

  const handleOnSubmit = () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async (_, setError) => {
      const {
        name, algorithm, frameworks, modelType, granularity,
      } = formStepOne;

      const response = await triggerAddNewModel({
        name,
        dataType: DataTypeEnum.TEXT,
        modelType,
        granularity,
        algorithm,
        frameworks,
      });

      if (response.error) {
        console.error(response.error);
        setError('silent.backed', response.error);
        return;
      }

      const newModelUUID = response.data.uuid;

      searchParams.delete('modal');
      dispatch(globalConfigSliceActions.addModelToShowConfettiList(newModelUUID));

      navigate({ pathname: `models/${response.data.uuid}`, search: searchParams.toString() });
    });
  };

  return { handleOnSubmit, args, isSubmitDisabled };
};
