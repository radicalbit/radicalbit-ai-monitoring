import { Button } from '@radicalbit/radicalbit-design-system';
import { useModalContext } from '../modal-context-provider';
import useHandleOnNext from './use-handle-on-next';

function Actions() {
  const { setStep } = useModalContext();

  const { handleOnNext, args, isSubmitDisabled } = useHandleOnNext();

  const handleOnPrev = () => {
    setStep((s) => s - 1);
  };

  return (
    <>
      <Button onClick={handleOnPrev}>Prev</Button>

      <Button
        disabled={isSubmitDisabled}
        loading={args.isLoading}
        onClick={handleOnNext}
        type="primary"
      >
        Next
      </Button>
    </>
  );
}

export default Actions;
