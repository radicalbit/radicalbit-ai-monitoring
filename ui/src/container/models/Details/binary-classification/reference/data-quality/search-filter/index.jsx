import { modelsApiSlice } from '@State/models/api';
import { fa1, faSearch } from '@fortawesome/free-solid-svg-icons';
import { useFormbitContext } from '@radicalbit/formbit';
import {
  Button, FontAwesomeIcon, FormField, Select, Toggle,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';

const { useGetReferenceDataQualityQuery } = modelsApiSlice;

function SearchFeatureList() {
  const { uuid } = useParams();
  const { write } = useFormbitContext();

  const { data } = useGetReferenceDataQualityQuery({ uuid });
  const items = data?.dataQuality.featureMetrics ?? [];
  const options = items.map((i) => ({ label: i.featureName, value: i.featureName }));

  const handleOnSelect = (value) => {
    write('__metadata.selectedFeatures', value);
  };

  return (
    <div className="flex flex-row w-full gap-4 mt-4">
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
                  available features

                </div>

                <FontAwesomeIcon icon={faSearch} />

              </div>
            )}
          />
        </FormField>
      </div>

      <NumericalFilter />

      <CategoricalFilter />
    </div>
  );
}

function NumericalFilter() {
  const { form, write } = useFormbitContext();
  const { __metadata: { isNumericalSelected } } = form;

  const type = isNumericalSelected ? 'primary' : 'secondary';
  const title = isNumericalSelected ? 'Numerical' : 'Show numerical';

  const handleOnClick = () => {
    write('__metadata.isNumericalSelected', !isNumericalSelected);
  };

  return (
    <Tooltip title={title}>
      <Toggle checked={isNumericalSelected} onClick={handleOnClick}>
        <Button
          shape="circle"
          title="1"
          type={type}
        >
          <FontAwesomeIcon icon={fa1} />
        </Button>
      </Toggle>
    </Tooltip>
  );
}

function CategoricalFilter() {
  const { form, write } = useFormbitContext();
  const { __metadata: { isCategoricalSelected } } = form;

  const type = isCategoricalSelected ? 'primary' : 'secondary';
  const title = isCategoricalSelected ? 'Categorical' : 'Show categorical';

  const handleOnClick = () => {
    write('__metadata.isCategoricalSelected', !isCategoricalSelected);
  };

  return (
    <Tooltip title={title}>
      <Toggle checked={isCategoricalSelected} onClick={handleOnClick}>
        <Button
          shape="circle"
          type={type}
        >
          C
        </Button>
      </Toggle>
    </Tooltip>
  );
}

export default SearchFeatureList;
