import { useGetCurrentDataQuality } from '@State/models/modal-hook';
import { fa1, faC, faSearch } from '@fortawesome/free-solid-svg-icons';
import { useFormbitContext } from '@radicalbit/formbit';
import {
  Button, FontAwesomeIcon, FormField, Select, Toggle,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';

function SearchFeatureList() {
  const { uuid } = useParams();
  const { write } = useFormbitContext();

  const { data } = useGetCurrentDataQuality({ uuid });
  const items = data?.dataQuality?.featureMetrics ?? [];
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
            placeholder={<FontAwesomeIcon icon={faSearch} />}
            style={{ width: '100%' }}
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
          onClick={handleOnClick}
          shape="circle"
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
          <FontAwesomeIcon icon={faC} />
        </Button>
      </Toggle>
    </Tooltip>
  );
}

export default SearchFeatureList;
