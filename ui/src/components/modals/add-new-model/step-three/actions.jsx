import { Button } from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import useHandleOnNext from './use-handle-on-next';
import { useModalContext } from '../modal-context-provider';

function Actions() {
  const { setStep } = useModalContext();
  const { handleOnNext, isSubmitDisabled } = useHandleOnNext();

  const handleOnPrev = () => {
    setStep((s) => s - 1);
  };

  return (
    <>
      <Button onClick={handleOnPrev}>Prev</Button>

      <Button
        disabled={isSubmitDisabled}
        onClick={handleOnNext}
        type="primary"
      >
        Next
      </Button>
    </>
  );
}

export default memo(Actions);
