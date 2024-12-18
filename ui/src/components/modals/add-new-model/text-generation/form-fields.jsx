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
import useHandleOnSubmit from './use-handle-on-submit';

function Name() {
  const ref = useRef(null);

  const { handleOnSubmit, isSubmitDisabled } = useHandleOnSubmit();
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
        onPressEnter={handleOnSubmit}
        readOnly={isSubmitDisabled}
        ref={ref}
        value={form.name}
      />
    </FormField>
  );
}

function ModelType() {
  const { useFormbit } = useModalContext();
  const { form, write } = useFormbit;

  const { isSubmitDisabled } = useHandleOnSubmit();

  const handleOnChange = (value) => {
    write('modelType', value);
  };

  const modelTypeSelections = [
    ModelTypeEnum.BINARY_CLASSIFICATION,
    ModelTypeEnum.MULTI_CLASSIFICATION,
    ModelTypeEnum.REGRESSION,
    ModelTypeEnum.TEXT_GENERATION,
  ];

  return (
    <FormField label="Model type" modifier="w-full" required>
      <Select onChange={handleOnChange} readOnly={isSubmitDisabled} value={form.modelType}>
        {Object.values(modelTypeSelections).map((value) => (
          <Select.Option key={value}>
            {ModelTypeEnumLabel[value]}
          </Select.Option>
        ))}
      </Select>
    </FormField>
  );
}

function DataType() {
  const { useFormbit } = useModalContext();
  const { error } = useFormbit;

  return (
    <FormField label="Data type" message={error('dataType')} modifier="w-full" required>
      {DataTypeEnumLabel[DataTypeEnum.TEXT]}
    </FormField>
  );
}

function Granularity() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const { isSubmitDisabled } = useHandleOnSubmit();

  const handleOnChange = (value) => {
    write('granularity', value);
  };

  return (
    <FormField label="Granularity" message={error('granularity')} modifier="w-full" required>
      <Select onChange={handleOnChange} readOnly={isSubmitDisabled} value={form.granularity}>
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
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const { handleOnSubmit, isSubmitDisabled } = useHandleOnSubmit();

  const handleOnChange = ({ target: { value } }) => {
    write('frameworks', value);
  };

  return (
    <FormField label="Framework" message={error('frameworks')} modifier="w-full">
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnSubmit}
        readOnly={isSubmitDisabled}
        value={form.frameworks}
      />
    </FormField>
  );
}

function Algorithm() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const { handleOnSubmit, isSubmitDisabled } = useHandleOnSubmit();

  const handleOnChange = ({ target: { value } }) => {
    write('algorithm', value);
  };

  return (
    <FormField label="Algorithm" message={error('algorithm')} modifier="w-full">
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnSubmit}
        readOnly={isSubmitDisabled}
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
