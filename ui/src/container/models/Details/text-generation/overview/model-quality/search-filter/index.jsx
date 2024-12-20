import { useGetCurrentDataQualityQueryWithPolling } from '@State/models/polling-hook';
import { fa1, faC, faSearch } from '@fortawesome/free-solid-svg-icons';
import { useFormbitContext } from '@radicalbit/formbit';
import {
  Button, FontAwesomeIcon, FormField, Input, Select, Toggle,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';

function SearchFeatureList() {
  const { write } = useFormbitContext();

  const { data } = useGetCurrentDataQualityQueryWithPolling();
  const items = data?.dataQuality?.featureMetrics ?? [];
  const options = items.map((i) => ({ label: i.featureName, value: i.featureName }));

  const handleOnSelect = (value) => {
    write('__metadata.selectedFeatures', value);
  };

  return (
    <div className="flex flex-row w-full gap-4 mt-4">
      <div className="w-full">
        <FormField>
          <Input
            onChange={handleOnSelect}
            options={options}
            placeholder={(
              <div className="flex flex-row items-center justify-between gap-4">
                <div>
                  Please select one or more of the
                  {' '}

                  {items.length}

                  {' '}
                  available features

                </div>

                <FontAwesomeIcon icon={faSearch} />

              </div>
            )}
            style={{ width: '100%' }}
          />
        </FormField>
      </div>

    </div>
  );
}

export default SearchFeatureList;
