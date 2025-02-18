import { DataTable } from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import { memo, useCallback } from 'react';
import columns from './columns';

function NumericalTable({ data }) {
  const leftTableData = useCallback((el) => [
    { label: 'Avg', value: el?.mean ?? '--' },
    { label: 'Std', value: el?.std ?? '--' },
    { label: 'Min', value: el?.min ?? '--' },
    { label: 'Max', value: el?.max ?? '--' },
  ].map((o) => ({ ...o, value: (o.value !== '--') ? numberFormatter().format(o.value) : '--' })), []);

  const centerTableData = useCallback((el) => [
    { label: 'Percentile 25', value: el?.medianMetrics?.perc25 ?? '--' },
    { label: 'Median', value: el?.medianMetrics?.median ?? '--' },
    { label: 'Percentile 75', value: el?.medianMetrics?.perc75 ?? '--' },
    { label: 'Missing values', value: `${numberFormatter().format(el?.missingValue?.count)} (${numberFormatter().format(el?.missingValue?.percentage)}%)` },
  ].map((o) => {
    if (o.label === 'Missing values') {
      return o;
    }
    return { ...o, value: (o.value !== '--') ? numberFormatter().format(o.value) : '--' };
  }), []);

  if (!data) {
    return false;
  }

  return (
    <div className="flex flex-row gap-4">
      <DataTable
        columns={columns}
        dataSource={leftTableData(data)}
        modifier="basis-1/3"
        noHead
        pagination={false}
        rowClassName={DataTable.ROW_NOT_CLICKABLE}
        rowHoverable={false}
        rowKey={({ label }) => label}
        size="small"
      />

      <DataTable
        columns={columns}
        dataSource={centerTableData(data)}
        modifier="basis-2/3"
        noHead
        pagination={false}
        rowClassName={DataTable.ROW_NOT_CLICKABLE}
        rowHoverable={false}
        rowKey={({ label }) => label}
        size="small"
      />

    </div>
  );
}

export default memo(NumericalTable);
