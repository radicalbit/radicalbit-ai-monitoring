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
    title: 'Name',
    key: 'name',
    activeFilters,
    activeSorter,
    width: '33%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Model Type',
    dataIndex: 'modelType',
    key: 'modelType',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '21%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Data Quality',
    key: 'dataQuality',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '10%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Model Quality',
    key: 'modelQuality',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '10%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Drift Quality',
    key: 'driftQuality',
    activeFilters,
    activeSorter,
    align: 'left',
    width: '10%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Updated',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
    activeFilters,
    activeSorter,
    sorter: false,
    align: 'right',
    width: '13%',
    render: () => (<Skeleton.Input active block />),
  }),
];
