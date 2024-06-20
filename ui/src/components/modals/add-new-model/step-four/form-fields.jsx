import { FormField, Select, Tooltip } from '@radicalbit/radicalbit-design-system';
import { ModelTypeEnum } from '@Src/store/state/models/constants';
import { useModalContext } from '../modal-context-provider';

function Target() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const targets = useGetTargets();
  const timestampName = form?.timestamp?.name;
  const value = form?.target?.name;

  const handleOnChange = (val) => {
    try {
      write('target', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
    }
  };

  return (
    <FormField
      label="Target"
      message={error('target')}
      modifier="w-full"
      required
    >
      <Select
        onChange={handleOnChange}
        placeholder="Pick a feature as target"
        showSearch
        value={value}
      >
        {targets.map((o) => {
          const { name, type } = o;
          const v = JSON.stringify(o);
          const isDisabled = timestampName === name;

          if (isDisabled) {
            return (
              <Select.Option key={name} disabled value={v}>
                <Tooltip placement="left" title="Already chosed as timestamp">
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type}) - current timestamp`}</small>
                  </div>
                </Tooltip>
              </Select.Option>
            );
          }

          return (
            <Select.Option key={name} value={v}>
              <div className="flex flex-row items-center gap-2">
                <div>{name}</div>

                <small>{`(${type})`}</small>
              </div>
            </Select.Option>
          );
        })}
      </Select>
    </FormField>
  );
}

function Timestamp() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const validTimestampFeatures = useGetTimestapValidFeatures();
  const targetName = form?.target?.name;
  const value = form?.timestamp?.name;

  const handleOnChange = (val) => {
    try {
      write('timestamp', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
    }
  };

  return (
    <FormField
      label="Timestamp"
      message={error('timestamp')}
      modifier="w-full"
      required
    >
      <Select
        onChange={handleOnChange}
        placeholder="Pick a variable as timestamp"
        showSearch
        value={value}
      >
        {validTimestampFeatures.map((o) => {
          const { name, type } = o;
          const v = JSON.stringify(o);
          const isDisabled = targetName === name;

          if (isDisabled) {
            return (
              <Select.Option key={name} disabled value={v}>
                <Tooltip placement="left" title="Already chosed as target">
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type}) - current target`}</small>
                  </div>
                </Tooltip>
              </Select.Option>
            );
          }

          return (
            <Select.Option key={name} value={v}>
              <div className="flex flex-row items-center gap-2">
                <div>{name}</div>

                <small>{`(${type})`}</small>
              </div>
            </Select.Option>
          );
        })}
      </Select>
    </FormField>
  );
}

function Prediction() {
  const { useFormbit } = useModalContext();
  const { form, error, write } = useFormbit;

  const predictions = useGetPredictions();
  const value = form?.prediction?.name;
  const predictionProbaName = form?.predictionProba?.name;

  const handleOnChange = (val) => {
    try {
      write('prediction', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
    }
  };

  return (
    <FormField
      label="Prediction"
      message={error('prediction')}
      modifier="w-full"
      required
    >
      <Select
        onChange={handleOnChange}
        placeholder="Pick an output as prediction"
        showSearch
        value={value}
      >
        {predictions.map((o) => {
          const { name, type } = o;
          const v = JSON.stringify(o);
          const isDisabled = predictionProbaName === name;

          if (isDisabled) {
            return (
              <Select.Option key={name} disabled value={v}>
                <Tooltip placement="left" title="Already chosed as probability">
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type}) - current probability`}</small>
                  </div>
                </Tooltip>
              </Select.Option>
            );
          }

          return (
            <Select.Option key={name} value={v}>
              <div className="flex flex-row items-center gap-2">
                <div>{name}</div>

                <small>{`(${type})`}</small>
              </div>
            </Select.Option>
          );
        })}
      </Select>
    </FormField>
  );
}

function Probability() {
  const { useFormbit } = useModalContext();
  const {
    form, error, write, remove,
  } = useFormbit;

  const probabilities = useGetProbabilities();
  const predictionName = form?.prediction?.name;
  const value = form?.predictionProba?.name;

  const handleOnChange = (val) => {
    if (val === undefined) {
      remove('predictionProba');
      return;
    }

    try {
      write('predictionProba', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
    }
  };

  return (
    <FormField
      label="Probability"
      message={error('predictionProba')}
      modifier="w-full"
    >
      <Select
        allowClear
        onChange={handleOnChange}
        placeholder="Pick an output as probability"
        showSearch
        value={value}
      >
        {probabilities.map((o) => {
          const { name, type } = o;
          const v = JSON.stringify(o);
          const isDisabled = predictionName === name;

          if (isDisabled) {
            return (
              <Select.Option key={name} disabled value={v}>
                <Tooltip placement="left" title="Already chosed as prediction">
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type}) - current prediction`}</small>
                  </div>
                </Tooltip>
              </Select.Option>
            );
          }

          return (
            <Select.Option key={name} value={v}>
              <div className="flex flex-row items-center gap-2">
                <div>{name}</div>

                <small>{`(${type})`}</small>
              </div>
            </Select.Option>
          );
        })}
      </Select>
    </FormField>
  );
}

const targetValidTypes = ['int', 'float', 'double'];
const useGetTargets = () => {
  const { useFormbit } = useModalContext();
  const { form } = useFormbit;

  return form.features.filter(({ type }) => targetValidTypes.includes(type));
};

const predictionValidTypes = ['int', 'float', 'double'];
const useGetPredictions = () => {
  const { useFormbit } = useModalContext();
  const { form } = useFormbit;

  return form.outputs.filter(({ type }) => predictionValidTypes.includes(type));
};

const binaryClassificationProbabilityValidTypes = ['float', 'double'];
const useGetProbabilities = () => {
  const { useFormbitStepOne, useFormbit } = useModalContext();
  const { form } = useFormbit;
  const { form: formStepOne } = useFormbitStepOne;

  if (formStepOne.modelType === ModelTypeEnum.BINARY_CLASSIFICATION) {
    return form.outputs.filter(({ type }) => binaryClassificationProbabilityValidTypes.includes(type));
  }

  return form.outputs;
};

const timestampValidTypes = ['datetime'];
const useGetTimestapValidFeatures = () => {
  const { useFormbitStepOne, useFormbit } = useModalContext();
  const { form } = useFormbit;
  const { form: formStepOne } = useFormbitStepOne;

  if (formStepOne.modelType === ModelTypeEnum.BINARY_CLASSIFICATION) {
    return form?.features.filter(({ type }) => timestampValidTypes.includes(type));
  }

  return form.outputs;
};

export {
  Prediction, Probability, Target, Timestamp,
};
