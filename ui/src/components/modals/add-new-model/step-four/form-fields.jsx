import { ModelTypeEnum } from '@Src/store/state/models/constants';
import {
  FormField,
  Select,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { grafanaTracking } from '@Src/main';
import { useModalContext } from '../modal-context-provider';

function Target() {
  const { useFormbit } = useModalContext();
  const {
    form, error, write, remove,
  } = useFormbit;

  const targets = useGetTargets();
  const timestampName = form?.timestamp?.name;
  const predictionName = form?.prediction?.name;
  const predictionProbaName = form?.predictionProba?.name;
  const value = form?.target?.name;

  const handleOnChange = (val) => {
    if (!val) {
      remove('target');
      return;
    }

    try {
      write('target', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
      grafanaTracking?.api.pushError(e);
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

          switch (name) {
            case timestampName:
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
            case predictionName:
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
            case predictionProbaName:
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
            default:
              return (
                <Select.Option key={name} value={v}>
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type})`}</small>
                  </div>
                </Select.Option>
              );
          }
        })}
      </Select>
    </FormField>
  );
}

function Timestamp() {
  const { useFormbit } = useModalContext();
  const {
    form, error, write, remove,
  } = useFormbit;

  const validTimestampFeatures = useGetTimestapValidFeatures();
  const targetName = form?.target?.name;
  const predictionName = form?.prediction?.name;
  const predictionProbaName = form?.predictionProba?.name;
  const value = form?.timestamp?.name;

  const handleOnChange = (val) => {
    if (!val) {
      remove('timestamp');
      return;
    }

    try {
      write('timestamp', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
      grafanaTracking?.api.pushError(e);
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

          switch (name) {
            case targetName:
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
            case predictionName:
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
            case predictionProbaName:
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
            default:
              return (
                <Select.Option key={name} value={v}>
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type})`}</small>
                  </div>
                </Select.Option>
              );
          }
        })}
      </Select>
    </FormField>
  );
}

function Prediction() {
  const { useFormbit } = useModalContext();
  const {
    form, error, write, remove,
  } = useFormbit;

  const predictions = useGetPredictions();
  const value = form?.prediction?.name;
  const predictionProbaName = form?.predictionProba?.name;
  const timestampName = form?.timestamp?.name;
  const targetName = form?.target?.name;

  const handleOnChange = (val) => {
    if (!val) {
      remove('prediction');
      return;
    }

    try {
      write('prediction', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
      grafanaTracking?.api.pushError(e);
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

          switch (name) {
            case targetName:
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
            case timestampName:
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
            case predictionProbaName:
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
            default:
              return (
                <Select.Option key={name} value={v}>
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type})`}</small>
                  </div>
                </Select.Option>
              );
          }
        })}
      </Select>
    </FormField>
  );
}

function Probability() {
  const { useFormbit, useFormbitStepOne } = useModalContext();

  const {
    form, error, write, remove,
  } = useFormbit;
  const probabilities = useGetProbabilities();
  const predictionName = form?.prediction?.name;
  const timestampName = form?.timestamp?.name;
  const targetName = form?.target?.name;
  const value = form?.predictionProba?.name;

  const { form: formStepOne } = useFormbitStepOne;
  const { modelType } = formStepOne;

  const handleOnChange = (val) => {
    if (!val) {
      remove('predictionProba');
      return;
    }

    try {
      write('predictionProba', JSON.parse(val));
    } catch (e) {
      console.error('Error in parsing Select.Option value: ', e);
      grafanaTracking?.api.pushError(e);
    }
  };

  if (modelType === ModelTypeEnum.REGRESSION) {
    return (
      <FormField label="Probability" modifier="w-full">
        <Select disabled readOnly value="Not available for Regression" />
      </FormField>
    );
  }

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

          switch (name) {
            case targetName:
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
            case timestampName:
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
            case predictionName:
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
            default:
              return (
                <Select.Option key={name} value={v}>
                  <div className="flex flex-row items-center gap-2">
                    <div>{name}</div>

                    <small>{`(${type})`}</small>
                  </div>
                </Select.Option>
              );
          }
        })}
      </Select>
    </FormField>
  );
}

const targetValidTypes = {
  [ModelTypeEnum.BINARY_CLASSIFICATION]: ['int', 'float', 'double'],
  [ModelTypeEnum.MULTI_CLASSIFICATION]: ['int', 'float', 'double', 'string'],
  [ModelTypeEnum.REGRESSION]: ['int', 'float', 'double'],
};
const useGetTargets = () => {
  const { useFormbit, useFormbitStepOne } = useModalContext();
  const { form } = useFormbit;
  const predictionType = form?.prediction?.type;

  const { form: formStepOne } = useFormbitStepOne;
  const { modelType } = formStepOne;

  return form.outputs.filter(({ type }) => {
    if (predictionType) {
      return type === predictionType;
    }

    return targetValidTypes[modelType].includes(type);
  });
};

const predictionValidTypes = {
  [ModelTypeEnum.BINARY_CLASSIFICATION]: ['int', 'float', 'double'],
  [ModelTypeEnum.MULTI_CLASSIFICATION]: ['int', 'float', 'double', 'string'],
  [ModelTypeEnum.REGRESSION]: ['int', 'float', 'double'],
};
const useGetPredictions = () => {
  const { useFormbit, useFormbitStepOne } = useModalContext();
  const { form } = useFormbit;
  const targetType = form?.target?.type;

  const { form: formStepOne } = useFormbitStepOne;
  const { modelType } = formStepOne;

  return form.outputs.filter(({ type }) => {
    if (targetType) {
      return type === targetType;
    }

    return predictionValidTypes[modelType].includes(type);
  });
};

const probabilityValidTypes = {
  [ModelTypeEnum.BINARY_CLASSIFICATION]: ['float', 'double'],
  [ModelTypeEnum.MULTI_CLASSIFICATION]: ['float', 'double', 'string'],
  [ModelTypeEnum.REGRESSION]: ['float', 'double'],
};
const useGetProbabilities = () => {
  const { useFormbitStepOne, useFormbit } = useModalContext();
  const { form } = useFormbit;

  const { form: formStepOne } = useFormbitStepOne;
  const { modelType } = formStepOne;

  return form.outputs.filter(({ type }) => probabilityValidTypes[modelType].includes(type));
};

const timestampValidTypes = {
  [ModelTypeEnum.BINARY_CLASSIFICATION]: ['datetime'],
  [ModelTypeEnum.MULTI_CLASSIFICATION]: ['datetime'],
  [ModelTypeEnum.REGRESSION]: ['datetime'],
};
const useGetTimestapValidFeatures = () => {
  const { useFormbitStepOne, useFormbit } = useModalContext();
  const { form } = useFormbit;

  const { form: formStepOne } = useFormbitStepOne;
  const { modelType } = formStepOne;

  return form?.outputs.filter(({ type }) => timestampValidTypes[modelType].includes(type));
};

export {
  Prediction, Probability, Target, Timestamp,
};
