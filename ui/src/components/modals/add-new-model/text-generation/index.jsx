import {
  Button, FormField, SectionTitle, Spinner,
} from '@radicalbit/radicalbit-design-system';
import {
  Algorithm, DataType, Framework, Granularity, ModelType, Name,
} from './form-fields';
import { useModalContext } from '../modal-context-provider';
import useHandleOnSubmit from './use-handle-on-submit';

function TextGenerationHeader() {
  return <SectionTitle align="center" title="New Model" titleColor="primary" />;
}

function TextGenerationBody() {
  const { useFormbit } = useModalContext();
  const { error } = useFormbit;

  return (
    <div className="w-full flex justify-center">
      <Spinner isFormWrapper modifier="max-w-[400px]">
        <Name />

        <div className="flex flex-row gap-4 w-full">
          <ModelType />

          <DataType />
        </div>

        <Granularity />

        <Framework />

        <Algorithm />

        {error('silent.backend') && <FormField message={error('silent.backend')} />}
      </Spinner>

    </div>

  );
}

function TextGenerationActionButton() {
  const { handleOnSubmit, args, isSubmitDisabled } = useHandleOnSubmit();

  return (
    <>
      <div />

      <Button
        disabled={isSubmitDisabled}
        loading={args.isLoading}
        onClick={handleOnSubmit}
        type="primary"
      >
        Save Model
      </Button>
    </>
  );
}

export { TextGenerationHeader, TextGenerationBody, TextGenerationActionButton };
