import { Button, FormField, SectionTitle } from '@radicalbit/radicalbit-design-system';
import {
  Algorithm, DataType, Framework, Granularity, ModelType, Name,
} from './form-fields';
import { useModalContext } from '../modal-context-provider';
import useHandleOnSubmit from './use-handle-on-submit';

function LlmHeader() {
  return <SectionTitle title="New Model" />;
}

function LlmBody() {
  const { useFormbit } = useModalContext();
  const { error } = useFormbit;

  return (
    <div className="flex flex-row justify-center">
      <div className="flex flex-col gap-4 w-full max-w-[400px] items-center">
        <Name />

        <div className="flex flex-row gap-4 w-full">
          <ModelType />

          <DataType />
        </div>

        <Granularity />

        <Framework />

        <Algorithm />

        <FormField message={error('silent.backend')} />
      </div>
    </div>

  );
}

function LlmActionButton() {
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

export { LlmHeader, LlmBody, LlmActionButton };
