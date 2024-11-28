import { Skeleton } from '@radicalbit/radicalbit-design-system';
import { columnFactory } from '@Src/components/smart-table/utils';

const getSkeletonColumns = (
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
    width: '51%',
    render: () => (<Skeleton.Input active block />),
  }),

  columnFactory({
    title: 'Updated',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
    activeFilters,
    activeSorter,
    sorter: true,
    align: 'right',
    width: '13%',
    render: () => (<Skeleton.Input active block />),
  }),
];

export default getSkeletonColumns;
