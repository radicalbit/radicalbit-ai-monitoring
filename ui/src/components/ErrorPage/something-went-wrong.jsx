import Logo from '@Img/logo.png';
import { Void } from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';

function SomethingWentWrong({ size }) {
  return (
    <Void
      description={(
        <>
          We are sorry
          <br />
          we are experiencing some errors in our infrastructure
        </>
      )}
      image={<img alt="500" src={Logo} />}
      size={size}
      title={(
        <>
          Oh no!
          <br />
          Something went wrong
        </>
      )}
    />
  );
}

export default memo(SomethingWentWrong);
