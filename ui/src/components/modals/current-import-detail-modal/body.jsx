import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useParams, useSearchParams } from 'react-router-dom';
import { METRICS_TABS } from '@Container/models/Details/constants';
import BinaryClassificationDataQualityMetrics from '@Container/models/Details/binary-classification/current/data-quality';
import BinaryClassificationModelQualityMetrics from '@Container/models/Details/binary-classification/current/model-quality';
import BinaryClassificationDataDriftMetrics from '@Container/models/Details/binary-classification/current/data-drift';
import MultiClassificationDataQualityMetrics from '@Container/models/Details/multi-classification/current/data-quality';
import MultiClassificationModelQualityMetrics from '@Container/models/Details/multi-classification/current/model-quality';
import MultiClassificationDataDriftMetrics from '@Container/models/Details/multi-classification/current/data-drift';
import RegressionDataQualityMetrics from '@Container/models/Details/regression/current/data-quality';
import RegressionModelQualityMetrics from '@Container/models/Details/regression/current/model-quality';
import RegressionDataDriftMetrics from '@Container/models/Details/regression/current/data-drift';
import { modelsApiSlice } from '@State/models/api';
import { ModelTypeEnum } from '@State/models/constants';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function Body() {
  const [searchParams, setSearchParams] = useSearchParams();

  const activeTab = searchParams.get('modal-tab-metrics') || METRICS_TABS.METRICS;

  const setTab = (value) => {
    searchParams.set('modal-tab-metrics', value);
    setSearchParams(searchParams);
  };

  const onChangeTab = (e) => {
    setTab(e);
  };

  const tabs = useGetTabs();

  return (
    <Tabs
      activeKey={activeTab}
      fullHeight
      items={tabs}
      noBorder
      onChange={onChangeTab}
    />
  );
}

function useGetTabs() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const modelType = data?.modelType;

  switch (modelType) {
    case ModelTypeEnum.BINARY_CLASSIFICATION:
      return [
        {
          label: METRICS_TABS.DATA_QUALITY,
          key: METRICS_TABS.DATA_QUALITY,
          children: <BinaryClassificationDataQualityMetrics />,
        },
        {
          label: METRICS_TABS.MODEL_QUALITY,
          key: METRICS_TABS.MODEL_QUALITY,
          children: <BinaryClassificationModelQualityMetrics />,
        },
        {
          label: METRICS_TABS.DATA_DRIFT,
          key: METRICS_TABS.DATA_DRIFT,
          children: <BinaryClassificationDataDriftMetrics />,
        },
      ];

    case ModelTypeEnum.MULTI_CLASSIFICATION:
      return [
        {
          label: METRICS_TABS.DATA_QUALITY,
          key: METRICS_TABS.DATA_QUALITY,
          children: <MultiClassificationDataQualityMetrics />,
        },
        {
          label: METRICS_TABS.MODEL_QUALITY,
          key: METRICS_TABS.MODEL_QUALITY,
          children: <MultiClassificationModelQualityMetrics />,
        },
        {
          label: METRICS_TABS.DATA_DRIFT,
          key: METRICS_TABS.DATA_DRIFT,
          children: <MultiClassificationDataDriftMetrics />,
        },
      ];

    case ModelTypeEnum.REGRESSION:
      return [
        {
          label: METRICS_TABS.DATA_QUALITY,
          key: METRICS_TABS.DATA_QUALITY,
          children: <RegressionDataQualityMetrics />,
        },
        {
          label: METRICS_TABS.MODEL_QUALITY,
          key: METRICS_TABS.MODEL_QUALITY,
          children: <RegressionModelQualityMetrics />,
        },
        {
          label: METRICS_TABS.DATA_DRIFT,
          key: METRICS_TABS.DATA_DRIFT,
          children: <RegressionDataDriftMetrics />,
        },
      ];
    default:
      return false;
  }
}

export default Body;
