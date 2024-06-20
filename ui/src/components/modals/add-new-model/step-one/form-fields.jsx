import useAutoFocus from '@Src/hooks/use-auto-focus';
import {
  DataTypeEnum, DataTypeEnumLabel, GranularityEnum, GranularityEnumLabel,
  ModelTypeEnum,
  ModelTypeEnumLabel,
} from '@State/models/constants';
import {
  FormField,
  Input,
  Select,
} from '@radicalbit/radicalbit-design-system';
import { useRef } from 'react';
import { useModalContext } from '../modal-context-provider';
import useHandleOnNext from './use-handle-on-next';

function Name() {
  const ref = useRef(null);

  const { handleOnNext } = useHandleOnNext();
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const handleOnChange = ({ target: { value } }) => {
    write('name', value);
  };

  useAutoFocus(ref);

  return (
    <FormField label="Name" message={error('name')} modifier="w-full" required>
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnNext}
        ref={ref}
        value={form.name}
      />
    </FormField>
  );
}

function ModelType() {
  return (
    <FormField label="Model type" modifier="w-full" required>
      {ModelTypeEnumLabel[ModelTypeEnum.BINARY_CLASSIFICATION]}
    </FormField>
  );
}

function DataType() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const handleOnChange = (value) => {
    write('dataType', value);
  };

  return (
    <FormField label="Data type" message={error('dataType')} modifier="w-full" required>
      <Select onChange={handleOnChange} value={form.dataType}>
        {Object.values(DataTypeEnum).map((value) => (
          <Select.Option key={value}>
            {DataTypeEnumLabel[value]}
          </Select.Option>
        ))}
      </Select>
    </FormField>
  );
}

function Granularity() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const handleOnChange = (value) => {
    write('granularity', value);
  };

  return (
    <FormField label="Granularity" message={error('granularity')} modifier="w-full" required>
      <Select onChange={handleOnChange} value={form.granularity}>
        {Object.values(GranularityEnum).map((value) => (
          <Select.Option key={value}>
            {GranularityEnumLabel[value]}
          </Select.Option>
        ))}
      </Select>
    </FormField>
  );
}

function Framework() {
  const { handleOnNext } = useHandleOnNext();
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const handleOnChange = ({ target: { value } }) => {
    write('frameworks', value);
  };

  return (
    <FormField label="Framework" message={error('frameworks')} modifier="w-full">
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnNext}
        value={form.frameworks}
      />
    </FormField>
  );
}

function Algorithm() {
  const { handleOnNext } = useHandleOnNext();
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const handleOnChange = ({ target: { value } }) => {
    write('algorithm', value);
  };

  return (
    <FormField label="Algorithm" message={error('algorithm')} modifier="w-full">
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnNext}
        value={form.algorithm}
      />
    </FormField>
  );
}

export {
  Algorithm,
  DataType,
  Framework,
  Granularity,
  ModelType,
  Name,
};
