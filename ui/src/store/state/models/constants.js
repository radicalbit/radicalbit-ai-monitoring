export const ModelTypeEnum = {
  REGRESSION: 'REGRESSION',
  BINARY_CLASSIFICATION: 'BINARY',
  MULTI_CLASSIFICATION: 'MULTI_CLASS',
  TEXT_GENERATION: 'TEXT_GENERATION',
  EMBEDDINGS: 'EMBEDDINGS',
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
  [ModelTypeEnum.TEXT_GENERATION]: 'Text Generation',
  [ModelTypeEnum.EMBEDDINGS]: 'Embeddings',
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
