import useModals from '@Hooks/use-modals';
import { RbitModal } from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import Body from './body';
import Header from './header';

function TraceDetailModal() {
  const { hideModal } = useModals();

  const handleOnCancel = () => {
    hideModal();
  };

  return (
    <RbitModal
      closeIcon={false}
      header={<Header />}
      headerType="light"
      maximize
      onCancel={handleOnCancel}
      open
    >
      <Body />
    </RbitModal>
  );
}

export default memo(TraceDetailModal);
