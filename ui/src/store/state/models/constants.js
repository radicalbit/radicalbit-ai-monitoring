export const ModelTypeEnum = {
  REGRESSION: 'REGRESSION',
  BINARY_CLASSIFICATION: 'BINARY',
  MULTI_CLASSIFICATION: 'MULTI_CLASS',
};

export const DataTypeEnum = {
  TABULAR: 'TABULAR',
  TEXT: 'TEXT',
  IMAGE: 'IMAGE',
};

export const GranularityEnum = {
  HOUR: 'HOUR',
  DAY: 'DAY',
  WEEK: 'WEEK',
  MONTH: 'MONTH',
};

export const ModelTypeEnumLabel = {
  [ModelTypeEnum.REGRESSION]: 'Regression',
  [ModelTypeEnum.BINARY_CLASSIFICATION]: 'Binary Classification',
  [ModelTypeEnum.MULTI_CLASSIFICATION]: 'Multiclass Classification',
};

export const DataTypeEnumLabel = {
  [DataTypeEnum.TABULAR]: 'Tabular',
  [DataTypeEnum.TEXT]: 'Text',
  [DataTypeEnum.IMAGE]: 'Image',
};

export const GranularityEnumLabel = {
  [GranularityEnum.HOUR]: 'Hour',
  [GranularityEnum.DAY]: 'Day',
  [GranularityEnum.WEEK]: 'Week',
  [GranularityEnum.MONTH]: 'Month',
};
