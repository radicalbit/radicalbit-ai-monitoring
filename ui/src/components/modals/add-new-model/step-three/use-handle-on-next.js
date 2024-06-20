import { useCallback } from 'react';
import { useModalContext } from '../modal-context-provider';

export default () => {
  const {
    useFormbit, useFormbitStepFour, step, setStep,
  } = useModalContext();

  const { initialize: initializeStepFour } = useFormbitStepFour;

  const {
    submitForm, isFormInvalid, form, isDirty, write,
  } = useFormbit;
  const variables = form?.variables;
  const outputKeys = form?.outputKeys;
  const featureKeys = form?.featureKeys;
  const { clearFieldNextStep } = form.__metadata;
  const isSubmitDisabled = isFormInvalid() || !isDirty;

  const handleOnNext = useCallback(() => {
    if (isSubmitDisabled) {
      return;
    }

    submitForm(() => {
      const outputs = outputKeys.reduce((acc, element) => {
        const el = variables.find((f) => f.name === element);
        return acc.concat(el);
      }, []);

      const features = featureKeys.reduce((acc, element) => {
        const el = variables.find((f) => f.name === element);
        return acc.concat(el);
      }, []);

      if (clearFieldNextStep) {
        write('__metadata.clearFieldNextStep', false);

        initializeStepFour(
          {
            outputs,
            features,
            timestamp: undefined,
            target: undefined,
            prediction: undefined,
            predictionProba: undefined,
          },
        );
      }

      setStep(step + 1);
    });
  }, [clearFieldNextStep, featureKeys, initializeStepFour, isSubmitDisabled, outputKeys, setStep, step, submitForm, variables, write]);

  return { handleOnNext, isSubmitDisabled };
};
