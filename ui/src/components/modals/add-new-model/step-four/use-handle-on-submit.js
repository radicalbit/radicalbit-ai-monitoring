import { modelsApiSlice } from '@State/models/api';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { useModalContext } from '../modal-context-provider';

const { useAddNewModelMutation } = modelsApiSlice;

export default () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const { useFormbit, useFormbitStepOne } = useModalContext();

  const { isDirty, isFormInvalid, submitForm } = useFormbit;
  const { form: formStepOne } = useFormbitStepOne;

  const [triggerAddNewModel, args] = useAddNewModelMutation();

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnSubmit = () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({
      form: {
        features, outputs, prediction, predictionProba, target, timestamp,
      },
    }, setError) => {
      const {
        name, algorithm, frameworks, modelType, dataType, granularity,
      } = formStepOne;

      const featuresWithoutTarget = features.filter((f) => f.name !== target.name);
      const featuresWithoutTimestamp = featuresWithoutTarget.filter((f) => f.name !== timestamp.name);

      const response = await triggerAddNewModel({
        name,
        dataType,
        modelType,
        granularity,
        algorithm,
        frameworks,
        features: featuresWithoutTimestamp,
        outputs: {
          prediction,
          predictionProba,
          output: outputs,
        },
        timestamp,
        target,
      });

      if (response.error) {
        console.error(response.error);
        setError('silent.backed', response.error);
        return;
      }

      searchParams.delete('modal');
      navigate({ pathname: `models/${response.data.uuid}`, search: searchParams.toString() });
    });
  };

  return { handleOnSubmit, args, isSubmitDisabled };
};
