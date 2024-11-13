export const MODEL_TABS_ENUM = {
  OVERVIEW: 'overview',
  REFERENCE_DASHBOARD: 'reference_dashboard',
  CURRENT_DASHBOARD: 'current_dashboard',
};

export const METRICS_TABS = {
  DATA_QUALITY: 'Data Quality',
  MODEL_QUALITY: 'Model Quality',
  DATA_DRIFT: 'Data Drift',
  IMPORT: 'Import',
};

export const OVERVIEW_TABS_ENUM = {
  SUMMARY: 'summary',
  VARIABLES: 'variables',
  OUTPUTS: 'outputs',
};

export const OVERVIEW_ROW_TYPE = {
  PROBABILITY: 'PROBABILITY',
  PREDICTION: 'PREDICTION',
  GROUND_TRUTH: 'GROUND TRUTH',
  TIMESTAMP: 'TIMESTAMP',
};

export const FEATURE_TYPE = {
  NUMERICAL: 'numerical',
  CATEGORICAL: 'categorical',
};

export const MODEL_QUALITY_FIELD = {
  ACCURACY: 'Accuracy',
  PRECISION: 'Precision',
  RECALL: 'Recall',
  F1: 'F1',
  FALSE_POSITIVE_RATE: 'False positive rate',
  TRUE_POSITIVE_RATE: 'True positive rate',
  AREA_UNDER_ROC: 'AUC-ROC',
  AREA_UNDER_PR: 'PR AUC',
  MSE: 'Mean squared error',
  RMSE: 'Root mean squared error',
  MAE: 'Mean absolute error',
  MAPE: 'Mean absolute percentage error',
  R2: 'R-squared',
  ADJ_R2: 'Adjusted R-squared',
  VARIANCE: 'Variance',
  LOG_LOSS: 'Log loss',
};

export const TABLE_COLOR = {
  REFERENCE_COLUMN: '#fafafc3d',
  CURRENT_COLUMN: '#3695d936',
};
