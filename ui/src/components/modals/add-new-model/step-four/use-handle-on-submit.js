import { modelsApiSlice } from '@State/models/api';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { ModelTypeEnum } from '@State/models/constants';
import { FEATURE_TYPE } from '@Container/models/Details/constants';
import { useDispatch } from 'react-redux';
import { globalConfigSliceActions } from '@State/global-configuration/slice';
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

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnSubmit = () => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({
      form: {
        outputs, prediction, predictionProba, target, timestamp,
      },
    }, setError) => {
      const {
        name, algorithm, frameworks, modelType, dataType, granularity,
      } = formStepOne;

      const variables = predictionProba
        ? outputs.filter((f) => f.name !== target.name && f.name !== timestamp.name && f.name !== prediction.name && f.name !== predictionProba.name)
        : outputs.filter((f) => f.name !== target.name && f.name !== timestamp.name && f.name !== prediction.name);

      const realOutput = predictionProba
        ? outputs.filter((f) => f.name === prediction.name || f.name === predictionProba.name)
        : outputs.filter((f) => f.name === prediction.name);

      const updatedTarget = {
        ...target,
        fieldType: (function getTargetFieldType(type) {
          switch (type) {
            case ModelTypeEnum.BINARY_CLASSIFICATION:
            case ModelTypeEnum.MULTI_CLASSIFICATION:
              return FEATURE_TYPE.CATEGORICAL;
            case ModelTypeEnum.REGRESSION:
              return FEATURE_TYPE.NUMERICAL;
            default:
              return '';
          }
        }(modelType)),
      };

      const response = await triggerAddNewModel({
        name,
        dataType,
        modelType,
        granularity,
        algorithm,
        frameworks,
        features: variables,
        outputs: {
          prediction,
          predictionProba,
          output: realOutput,
        },
        timestamp,
        target: updatedTarget,
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
