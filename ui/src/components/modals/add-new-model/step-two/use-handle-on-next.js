import { modelsApiSlice } from '@State/models/api';
import { useCallback } from 'react';
import { grafanaTracking } from '@Src/main';
import { useModalContext } from '../modal-context-provider';

const { useInferSchemaMutation } = modelsApiSlice;

const parseErrorMessage = (error) => {
  if (error?.data?.message) {
    return error.data.message;
  }

  if (error.status) {
    return `${error.status}: ${error.data}`;
  }

  return 'Something went wrong! Try again.';
};

export default () => {
  const [triggerInferSchema, args] = useInferSchemaMutation({ fixedCacheKey: 'infer-schema' });

  const {
    useFormbit, useFormbitStepThree, setStep, step,
  } = useModalContext();
  const { initialize: initializeStepThree } = useFormbitStepThree;
  const {
    submitForm, isFormInvalid, write, form, isDirty,
  } = useFormbit;
  const { clearFieldNextStep } = form.__metadata;

  const isSubmitDisabled = !isDirty || isFormInvalid();

  const handleOnNext = useCallback(() => {
    if (isSubmitDisabled || args.isLoading) {
      return;
    }

    submitForm(async ({ form: { file } }, setError) => {
      try {
        const { error, data } = await triggerInferSchema({ file });

        if (error) {
          const parsedErrorMessage = parseErrorMessage(error);

          console.error(error);

          setError('silent.backend', parsedErrorMessage);
          write('file', {
            ...file, name: file.name, status: 'error', response: parsedErrorMessage,
          });

          return;
        }

        if (clearFieldNextStep) {
          write('__metadata.clearFieldNextStep', false);

          initializeStepThree(
            {
              variables: data.inferred_schema,
              featureKeys: data.inferred_schema.map(({ name }) => name),
              outputKeys: [],
              __metadata: { clearFieldNextStep: true },
            },
          );
        }

        setStep(step + 1);
      } catch (e) {
        const parsedErrorMessage = parseErrorMessage(e);
        console.error(e);
        grafanaTracking?.api.pushError(e);

        setError('silent.backend', parsedErrorMessage);
        write('file', { ...form.file, status: 'error', response: parsedErrorMessage });
      }
    });
  }, [args.isLoading, clearFieldNextStep, form.file, initializeStepThree, isSubmitDisabled, setStep, step, submitForm, triggerInferSchema, write]);

  return { handleOnNext, args, isSubmitDisabled };
};
