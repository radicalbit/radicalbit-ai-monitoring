import { useFormbitContext } from '@radicalbit/formbit';
import {
  FormField, Input,
} from '@radicalbit/radicalbit-design-system';

function SearchFeatureList() {
  const { write } = useFormbitContext();

  const handleOnChange = ({ target: { value } }) => {
    write('__metadata.searchToken', value);
  };

  return (
    <div className="flex flex-row w-full gap-4 mt-4">
      <div className="w-full">
        <FormField>
          <Input
            allowClear
            onChange={handleOnChange}
            placeholder="Please select one or more of the available features"
            style={{ width: '100%' }}
          />
        </FormField>
      </div>

    </div>
  );
}

export default SearchFeatureList;
