import { FormbitContextProvider, useFormbitContext } from '@radicalbit/formbit';
import {
  DatePicker, FormField, Input,
} from '@radicalbit/radicalbit-design-system';
import { NamespaceEnum } from '@Src/constants';
import {
  selectors as contextConfigurationSelectors,
  thunks,
} from '@State/context-configuration';
import dayjs from 'dayjs';
import { isEmpty } from 'lodash';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from 'react-router-dom';
import schema from './schema';

function Filters() {
  const { externalFilters } = useSelector((state) => contextConfigurationSelectors.selectContextConfiguration(state, NamespaceEnum.SESSION_TRACES));

  return (
    <FormbitContextProvider initialValues={externalFilters} schema={schema}>
      <FiltersInner />
    </FormbitContextProvider>
  );
}

function FiltersInner() {
  const dispatch = useDispatch();
  const { form, write } = useFormbitContext();

  const [searchParams] = useSearchParams();
  const sessionUuid = searchParams.get('sessionUuid');

  useEffect(() => {
    if (sessionUuid) {
      write('sessionUuid', sessionUuid);
    }
  }, [sessionUuid, write]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (isEmpty(form)) {
        return;
      }

      dispatch(thunks.changeExternalFilters({ namespace: NamespaceEnum.SESSION_TRACES, externalFilters: form }));
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
  const { form, error } = useFormbitContext();
  const sessionUuid = form?.sessionUuid;

  return (
    <FormField label="SessionUuid" message={error('sessionUuid')} modifier="w-[310px]">
      <Input disabled value={sessionUuid} />
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
        minDate={fromTimestamp ? dayjs(fromTimestamp) : null}
        onChange={handleOnChange}
        onOk={handleOnChange}
        showTime
        value={toTimestamp ? dayjs(toTimestamp) : null}
      />
    </FormField>
  );
}

export default Filters;
