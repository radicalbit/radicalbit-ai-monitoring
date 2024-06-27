import { Tabs } from '@radicalbit/radicalbit-design-system';
import { useParams, useSearchParams } from 'react-router-dom';
import { METRICS_TABS } from '@Container/models/Details/constants';
import BinaryClassificationDataQualityMetrics from '@Container/models/Details/binary-classification/current/data-quality';
import BinaryClassificationModelQualityMetrics from '@Container/models/Details/binary-classification/current/model-quality';
import BinaryClassificationDataDriftMetrics from '@Container/models/Details/binary-classification/current/data-drift';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { ModelTypeEnum } from '@Src/store/state/models/constants';

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
    <div className="flex flex-col gap-4 h-full">
      <div className="px-4 pt-4 h-[99%]">
        <Tabs
          activeKey={activeTab}
          fullHeight
          items={tabs}
          onChange={onChangeTab}
        />
      </div>
    </div>
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
          label: METRICS_TABS.DATA_QUALITIY,
          key: METRICS_TABS.DATA_QUALITIY,
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

    default:
      return false;
  }
}

export default Body;
