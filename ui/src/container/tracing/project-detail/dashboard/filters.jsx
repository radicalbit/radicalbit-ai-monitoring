import { useFormbitContext } from '@radicalbit/formbit';
import { DatePicker, FormField } from '@radicalbit/radicalbit-design-system';
import dayjs from 'dayjs';

function Filters() {
  return (
    <div className="flex flex-row gap-2">
      <FromTimestampInput />

      <ToTimestampInput />
    </div>
  );
}

function FromTimestampInput() {
  const {
    form, write, error, validateForm, isFormInvalid,
  } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;

  const handleOnChange = (evt) => {
    write('fromTimestamp', evt, { successCallback: validateForm });
  };

  return (
    <FormField label="From timestamp" message={error('fromTimestamp')} required>
      <DatePicker
        onChange={handleOnChange}
        onOk={handleOnChange}
        showTime
        status={isFormInvalid() ? 'error' : undefined}
        value={fromTimestamp ? dayjs(fromTimestamp) : null}
      />
    </FormField>
  );
}

function ToTimestampInput() {
  const {
    form, write, error, validateForm, isFormInvalid,
  } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;
  const toTimestamp = form?.toTimestamp;

  const handleOnChange = (evt) => {
    write('toTimestamp', evt, { successCallback: validateForm });
  };

  return (
    <FormField label="To timestamp" message={error('toTimestamp')} required>
      <DatePicker
        minDate={fromTimestamp ? dayjs(fromTimestamp) : fromTimestamp}
        onChange={handleOnChange}
        onOk={handleOnChange}
        showTime
        status={isFormInvalid() ? 'error' : undefined}
        value={toTimestamp ? dayjs(toTimestamp) : null}
      />
    </FormField>
  );
}

export const filtersToQueryParams = (fromTimestamp, toTimestamp) => {
  const searchQueryParams = new URLSearchParams();

  if (fromTimestamp !== null) {
    searchQueryParams.set('fromTimestamp', dayjs(fromTimestamp).unix());
  }

  if (toTimestamp !== null) {
    searchQueryParams.set('toTimestamp', dayjs(toTimestamp).unix());
  }

  return searchQueryParams.toString();
};

export default Filters;
