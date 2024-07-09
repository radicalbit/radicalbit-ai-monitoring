import { useGetCurrentModelQualityQueryWithPolling, useGetReferenceModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { useFormbitContext } from '@radicalbit/formbit';

export default () => {
  const { form: { __metadata: { selectedCharts } } } = useFormbitContext();

  const { data: currentData } = useGetCurrentModelQualityQueryWithPolling();
  const { data: referenceData } = useGetReferenceModelQualityQueryWithPolling();

  const currentItems = currentData?.modelQuality?.classMetrics ?? [];
  const referenceItems = referenceData?.modelQuality?.classMetrics ?? [];

  const items = currentItems.map(({ className, ...currentRest }) => ({
    className,
    currentData: currentRest.groupedMetrics,
    referenceData: referenceItems.find((item) => item.className === className)?.metrics,
  }));

  return selectedCharts?.length > 0
    ? items.filter(({ className }) => selectedCharts.includes(className))
    : items;
};
