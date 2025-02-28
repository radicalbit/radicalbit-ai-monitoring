import { faM, faT } from '@fortawesome/free-solid-svg-icons';
import { useFormbitContext } from '@radicalbit/formbit';
import {
  Button,
  FontAwesomeIcon,
  FormField, Input,
  Toggle,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';

function SearchFeatureList() {
  const { form, write } = useFormbitContext();

  const isSearchForModelName = form?.__metadata.isSearchForModelName;
  const isSearchForTimestamp = form?.__metadata.isSearchForTimestamp;

  const handleOnChange = ({ target: { value } }) => {
    write('__metadata.searchToken', value);
  };

  const placeholder = !isSearchForModelName && !isSearchForTimestamp
    ? 'type a token for which to filter'
    : isSearchForModelName && !isSearchForTimestamp
      ? 'type the model name for which to filter'
      : !isSearchForModelName && isSearchForTimestamp
        ? 'type the timestamp for which to filter'
        : 'type a token for which to filter';

  return (
    <div className="flex flex-row w-full gap-4 mt-4">
      <div className="w-full">
        <FormField>
          <Input
            allowClear
            onChange={handleOnChange}
            placeholder={placeholder}
            style={{ width: '100%' }}
          />
        </FormField>
      </div>

      <ModelNameFilter />

      <TimestampFilter />

    </div>
  );
}

function ModelNameFilter() {
  const { form, write } = useFormbitContext();
  const { __metadata: { isSearchForModelName } } = form;

  const type = isSearchForModelName ? 'primary' : 'secondary';
  const title = isSearchForModelName ? 'Model name' : 'Filter by model name';

  const handleOnClick = () => {
    write('__metadata.isSearchForModelName', !isSearchForModelName);
  };

  return (
    <Tooltip title={title}>
      <Toggle checked={isSearchForModelName} onClick={handleOnClick}>
        <Button
          onClick={handleOnClick}
          shape="circle"
          title="1"
          type={type}
        >
          <FontAwesomeIcon icon={faM} />
        </Button>
      </Toggle>
    </Tooltip>
  );
}

function TimestampFilter() {
  const { form, write } = useFormbitContext();
  const { __metadata: { isSearchForTimestamp } } = form;

  const type = isSearchForTimestamp ? 'primary' : 'secondary';
  const title = isSearchForTimestamp ? 'Timestamp' : 'Filter by timestamp';

  const handleOnClick = () => {
    write('__metadata.isSearchForTimestamp', !isSearchForTimestamp);
  };

  return (
    <Tooltip title={title}>
      <Toggle checked={isSearchForTimestamp} onClick={handleOnClick}>
        <Button
          shape="circle"
          title="T"
          type={type}
        >
          <FontAwesomeIcon icon={faT} />
        </Button>
      </Toggle>
    </Tooltip>
  );
}

export default SearchFeatureList;
