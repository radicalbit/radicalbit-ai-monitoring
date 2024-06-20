import { FormField } from '@radicalbit/radicalbit-design-system';
import { useModalContext } from '../modal-context-provider';
import {
  Algorithm, DataType, Framework, Granularity, ModelType, Name,
} from './form-fields';

function Body() {
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

export default Body;
