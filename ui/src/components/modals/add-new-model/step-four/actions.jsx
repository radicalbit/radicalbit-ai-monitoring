import { Button } from '@radicalbit/radicalbit-design-system';
import { useModalContext } from '../modal-context-provider';
import useHandleOnSubmit from './use-handle-on-submit';

function Actions() {
  const { setStep } = useModalContext();

  const { handleOnSubmit, args, isSubmitDisabled } = useHandleOnSubmit();

  const handleOnPrev = () => {
    setStep((s) => s - 1);
  };

  return (
    <>
      <Button onClick={handleOnPrev}>Prev</Button>

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

export default Actions;
