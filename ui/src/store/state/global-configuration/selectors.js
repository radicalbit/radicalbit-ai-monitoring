import { createDraftSafeSelector } from '@reduxjs/toolkit';

const selectIsShowConfettiForModelCreation = createDraftSafeSelector(
  ({ globalConfiguration: { showConfettiFroModelCreation } }) => showConfettiFroModelCreation,
  (_, uuid) => uuid,
  (showConfettiFroModelCreation, uuid) => showConfettiFroModelCreation[uuid],
);

export { selectIsShowConfettiForModelCreation };
