import { FEATURE_TYPE } from '@Container/models/Details/constants';

export const pageSize = 20;
export const startPage = 1;
export const MAX_DECIMAL_ROUND = 3;
export const DEFAULT_POLLING_INTERVAL = 3000;
export const STATUS_SELECTOR_MAX_LEN = 10;
export const TRUNCATE_LENGTH = STATUS_SELECTOR_MAX_LEN + 3;

export const ModalsEnum = {
  QUERY_NAME: 'modal',
  ADD_NEW_MODEL: 'ADD_NEW_MODEL',
  IMPORT_DETAIL: 'IMPORT_DETAIL',
  IMPORT_ERRORS_DETAIL: 'IMPORT_ERRORS_DETAIL',
  CURRENT_IMPORT_DETAIL: 'CURRENT_IMPORT_DETAIL',
  COMPLETION_IMPORT_DETAIL: 'COMPLETION_IMPORT_DETAIL',
};

export const PathsEnum = {
  LAUNCHPAD: 'launchpad',
  MODELS: 'models',
  MODELS_DETAIL: 'models/:uuid',
};

export const ExternalPathsEnum = {
  BOOK_A_DEMO: 'https://radicalbit.ai/book-a-demo/',
  DOCUMENTATION: 'https://docs.oss-monitoring.radicalbit.ai',
  QUICKSTART: 'https://docs.oss-monitoring.radicalbit.ai/quickstart',
  IFRAME_VIDEO: 'https://www.youtube.com/embed/ujwyS8qGeaA?list=PLHWiJP04eQdoYLIO5kioLrO0Z7gIvEo3_',
  FREE_TRIAL: 'https://platform.radicalbit.ai/signUp/freemium',
};

export const PageEventsEnum = {
  CLEAR_GET_ALL_MODELS_INSTANCES_CACHE: 'clearGetAllModelsInstancesCache',
  CLEAR_GET_ALL_ALERTS_CACHE: 'clearGetAllAlertsCache',
  IS_COLLAPSED: 'isCollapsed',
  IS_OVERALL_TOP_COLLAPSED: 'isOverallTopCollapsed',
  CLEAR_GET_ALL_NOTIFICATIONS_CACHE: 'clearGetAllNotificationsCache',
};

export const SortOrderEnum = {
  ASCEND: 'ascend',
  DESCEND: 'descend',
};

export const NamespaceEnum = {
  MODELS_STATS: 'MODELS_STATS',
  MODELS: 'MODELS',
  REFERENCE_IMPORT: 'REFERENCE_IMPORT',
  CURRENT_IMPORT: 'CURRENT_IMPORT',
  COMPLETION_IMPORT: 'COMPLETION_IMPORT',
  ALERTS: 'ALERTS',
  MODELS_WIP: 'MODELS_WIP',
};

export const JOB_STATUS = {
  IMPORTING: 'IMPORTING',
  SUCCEEDED: 'SUCCEEDED',
  ERROR: 'ERROR',
  MISSING_REFERENCE: 'MISSING_REFERENCE',
  MISSING_CURRENT: 'MISSING_CURRENT',
  MISSING_COMPLETION: 'MISSING_COMPLETION',
};

export const NUMBER_FORMATTER_STYLE_ENUM = {
  DECIMAL: 'decimal',
  PERCENT: 'percent',
};

const defaultNumberFormatter = { maximumSignificantDigits: MAX_DECIMAL_ROUND, style: NUMBER_FORMATTER_STYLE_ENUM.DECIMAL };

export const numberFormatter = (options = defaultNumberFormatter) => new Intl.NumberFormat('en', options);

export const DRIFT_TEST_ENUM = {
  KS: 'KS',
  CHI2: 'CHI2',
  PSI: 'PSI',
};

export const DRIFT_TEST_ENUM_LABEL = {
  [DRIFT_TEST_ENUM.KS]: 'Kolmogorov-Smirnov (statistics)',
  [DRIFT_TEST_ENUM.CHI2]: 'Chi-Square Test (p-value)',
  [DRIFT_TEST_ENUM.PSI]: 'Population Stability Index',
};

// FIX: in the future the feature type comes from API
export const DRIFT_FEATURE_TYPE_ENUM = {
  [DRIFT_TEST_ENUM.KS]: FEATURE_TYPE.NUMERICAL,
  [DRIFT_TEST_ENUM.CHI2]: FEATURE_TYPE.CATEGORICAL,
  [DRIFT_TEST_ENUM.PSI]: FEATURE_TYPE.NUMERICAL,
};
