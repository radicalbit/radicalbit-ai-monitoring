import { Void } from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import LogoSquared from '@Img/logo-collapsed.svg';

function NoFeaturesAvailable() {
  return (
    <Void
      description={(
        <>
          Check filters or verify that there are features available in the dataset.
        </>
        )}
      image={<LogoSquared />}
      title="No feature available"
    />
  );
}

export default memo(NoFeaturesAvailable);
