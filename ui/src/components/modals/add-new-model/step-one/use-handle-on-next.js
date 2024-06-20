import { useCallback } from 'react';
import { useModalContext } from '../modal-context-provider';

export default () => {
  const { useFormbit, setStep, step } = useModalContext();
  const { submitForm, isFormInvalid, isDirty } = useFormbit;

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnNext = useCallback(() => {
    if (isSubmitDisabled) {
      return;
    }

    submitForm(() => {
      setStep(step + 1);
    });
  }, [isSubmitDisabled, setStep, step, submitForm]);

  return { handleOnNext, isSubmitDisabled };
};
