import { useGetCurrentModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { useFormbitContext } from '@radicalbit/formbit';
import {
  FontAwesomeIcon, FormField, Select,
} from '@radicalbit/radicalbit-design-system';

function SearchChart() {
  const { write } = useFormbitContext();
  const { data } = useGetCurrentModelQualityQueryWithPolling();

  const items = data?.modelQuality.classMetrics ?? [];
  const options = items.map(({ className }) => ({ label: className, value: className }));

  const handleOnSelect = (value) => {
    write('__metadata.selectedCharts', value);
  };

  return (
    <div className="flex flex-row w-full gap-4">
      <div className="w-full">
        <FormField>
          <Select
            mode="multiple"
            onChange={handleOnSelect}
            options={options}
            placeholder={(
              <div className="flex flex-row items-center justify-between gap-4">
                <div>
                  Please select one or more of the
                  {' '}

                  {items.length}

                  {' '}
                  available class

                </div>

                <FontAwesomeIcon icon={faSearch} />

              </div>
            )}
          />
        </FormField>
      </div>

    </div>
  );
}

export default SearchChart;
