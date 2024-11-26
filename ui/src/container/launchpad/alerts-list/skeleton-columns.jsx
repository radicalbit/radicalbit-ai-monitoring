import { columnFactory } from '@Src/components/smart-table/utils';
import { Skeleton } from '@radicalbit/radicalbit-design-system';

export const getSkeletonColumns = (
  activeFilters,
  activeSorter,
) => [
  columnFactory({
    title: 'S',
    key: 'name',
    width: '3%',
    align: 'center',
    render: () => (<Skeleton.Avatar active size="small" />),
  }),
  columnFactory({
    title: 'Section',
    key: 'anomalyType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '17%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Name',
    key: 'modelName',
    activeFilters,
    activeSorter,
    width: '16%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Features with anomalies',
    key: 'anomalyFeatures',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '64%',
    render: () => (<Skeleton.Input active block />),
  }),

];
