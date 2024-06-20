import { Board } from '@radicalbit/radicalbit-design-system';
import {
  Prediction, Probability, Target, Timestamp,
} from './form-fields';

function NewBody() {
  return (
    <div className="flex flex-row gap-8 justify-center items-center">

      <Board
        main={(
          <div className="flex flex-col gap-4 w-full">
            <Target />

            <Timestamp />
          </div>
          )}
        width={350}
      />

      <Board
        main={(
          <div className="flex flex-col gap-4 w-full">
            <Prediction />

            <Probability />
          </div>
          )}
        type="secondary"
        width={350}
      />

    </div>
  );
}

export default NewBody;
