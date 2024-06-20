import { Button } from '@radicalbit/radicalbit-design-system';
import useHandleOnNext from './use-handle-on-next';

function Actions() {
  const { handleOnNext, isSubmitDisabled } = useHandleOnNext();

  return (
    <>
      <div />

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

export default Actions;
