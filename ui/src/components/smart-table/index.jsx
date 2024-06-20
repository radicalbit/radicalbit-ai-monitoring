import { pageSize } from '@Src/constants';
import { selectors as contextConfigurationSelectors, thunks } from '@State/context-configuration';
import isEmpty from 'lodash/isEmpty';
import { DataTable } from '@radicalbit/radicalbit-design-system';
import { useDispatch, useSelector } from 'react-redux';

const { changeContextConfiguration } = thunks;

export default function SmartTable(props) {
  const {
    argumentsForColumns = [],
    columns: getColumns,
    namespace,
  } = props;

  const contextConfiguration = useSelector((state) => contextConfigurationSelectors.selectContextConfiguration(state, namespace));

  if (!contextConfiguration || !contextConfiguration.filters || !contextConfiguration.sorter) {
    console.error('Context configuration missing');
    return false;
  }

  const columns = getColumns(contextConfiguration.filters, contextConfiguration.sorter, ...argumentsForColumns);

  if (!columns || !Array.isArray(columns) || isEmpty(columns)) {
    console.error('Columns are not defined');
    return false;
  }

  return <SmartTableInner {...props} />;
}

function SmartTableInner({
  argumentsForColumns = [],
  clickable,
  columns: getColumns,
  components,
  dataSource,
  hasFixedColumn,
  loading,
  modifier,
  namespace,
  onRow,
  recordCount,
  rowClassName,
  rowKey,
  rowSelection,
}) {
  const dispatch = useDispatch();

  const contextConfiguration = useSelector((state) => contextConfigurationSelectors.selectContextConfiguration(state, namespace));

  const columns = getColumns(contextConfiguration.filters, contextConfiguration.sorter, ...argumentsForColumns);

  const handleTableChange = (currPagination, innerFilters, innerSorter) => {
    const { columnKey: field, order } = innerSorter;

    const sorterMapped = order && field ? { [field.toString()]: order } : {};

    const paginationOrElse = !isEmpty(currPagination) ? currPagination : contextConfiguration.pagination;

    const configuration = {
      pagination: paginationOrElse,
      filters: { ...innerFilters, ...contextConfiguration.filters }, // There might be other filter e.g. right columns search.
      sorter: sorterMapped,
    };

    dispatch(changeContextConfiguration({ namespace, configuration }));
  };

  const clonedPagination = contextConfiguration.pagination ? { ...contextConfiguration.pagination } : undefined;

  if (clonedPagination) {
    clonedPagination.total = recordCount || (dataSource && dataSource.length);
    clonedPagination.pageSize = contextConfiguration.pagination.pageSize || pageSize;
  }

  const showPagination = (recordCount || (dataSource && dataSource.length) || 0) > ((clonedPagination && clonedPagination.pageSize) || 0);

  return (
    <DataTable
      key={namespace}
      clickable={clickable}
      columns={columns}
      components={components}
      dataSource={dataSource}
      hasFixedColumn={hasFixedColumn}
      loading={loading}
      modifier={modifier}
      onChange={handleTableChange}
      onRow={onRow}
      pagination={showPagination && clonedPagination}
      rowClassName={rowClassName}
      rowKey={rowKey}
      rowSelection={rowSelection}
    />
  );
}
