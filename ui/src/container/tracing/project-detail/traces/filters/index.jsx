import { FormbitContextProvider, useFormbitContext } from '@radicalbit/formbit';
import {
  DatePicker, FormField, Input,
} from '@radicalbit/radicalbit-design-system';
import dayjs from 'dayjs';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import { isEmpty } from 'lodash';
import { NamespaceEnum } from '@Src/constants';
import {
  thunks, selectors as contextConfigurationSelectors,
} from '@State/context-configuration';
import schema from './schema';

function Filters() {
  const { externalFilters } = useSelector((state) => contextConfigurationSelectors.selectContextConfiguration(state, NamespaceEnum.TRACES_LIST));

  return (
    <FormbitContextProvider initialValues={externalFilters} schema={schema}>
      <FiltersInner />
    </FormbitContextProvider>
  );
}

function FiltersInner() {
  const dispatch = useDispatch();
  const { form } = useFormbitContext();

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (isEmpty(form)) {
        return;
      }

      dispatch(thunks.changeExternalFilters({ namespace: NamespaceEnum.TRACES_LIST, externalFilters: form }));
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [dispatch, form]);

  return (
    <div className="flex flex-row gap-2">
      <SessionUuidInput />

      <FromTimestampInput />

      <ToTimestampInput />

    </div>
  );
}

function SessionUuidInput() {
  const { form, write, error } = useFormbitContext();
  const sessionUuid = form?.sessionUuid;

  const handleOnChange = ({ target: { value } }) => {
    write('sessionUuid', value);
  };

  return (
    <FormField label="SessionUuid" message={error('sessionUuid')} modifier="w-[310px]">
      <Input
        onChange={handleOnChange}
        value={sessionUuid}
      />
    </FormField>
  );
}

function FromTimestampInput() {
  const { form, write, error } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;

  const handleOnChange = (evt) => {
    write('fromTimestamp', evt);
  };

  return (
    <FormField label="From timestamp" message={error('fromTimestamp')}>
      <DatePicker
        onChange={handleOnChange}
        onOk={handleOnChange}
        showTime
        value={fromTimestamp ? dayjs(fromTimestamp) : null}
      />
    </FormField>
  );
}

function ToTimestampInput() {
  const { form, write, error } = useFormbitContext();
  const fromTimestamp = form?.fromTimestamp;
  const toTimestamp = form?.toTimestamp;

  const handleOnChange = (evt) => {
    write('toTimestamp', evt);
  };

  return (
    <FormField label="To timestamp" message={error('toTimestamp')}>
      <DatePicker
        minDate={fromTimestamp}
        onChange={handleOnChange}
        onOk={handleOnChange}
        showTime
        value={toTimestamp ? dayjs(toTimestamp) : null}
      />
    </FormField>
  );
}

export default Filters;
