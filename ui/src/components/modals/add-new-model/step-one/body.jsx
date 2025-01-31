import { FormField, Spinner } from '@radicalbit/radicalbit-design-system';
import { useModalContext } from '../modal-context-provider';
import {
  Algorithm, DataType, Framework, Granularity, ModelType, Name,
} from './form-fields';

function Body() {
  const { useFormbit } = useModalContext();
  const { error } = useFormbit;

  return (
    <div className="w-full flex justify-center">
      <Spinner isFormWrapper modifier="max-w-[400px]">
        <Name />

        <div className="flex flex-row gap-4 w-full">
          <ModelType />

          <DataType />
        </div>

        <Granularity />

        <Framework />

        <Algorithm />

        {error('silent.backend') && <FormField message={error('silent.backend')} />}
      </Spinner>

    </div>
  );
}

export default Body;
