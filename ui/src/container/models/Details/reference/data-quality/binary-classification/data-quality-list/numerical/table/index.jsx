import { DataTable } from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import columns from './columns';

function NumericalTable({ data }) {
  if (!data) {
    return false;
  }

  const leftTableData = (el) => [
    { label: 'AVG', value: el?.mean ?? '--' },
    { label: 'STD', value: el?.std ?? '--' },
    { label: 'Min', value: el?.min ?? '--' },
    { label: 'Max', value: el?.max ?? '--' },
  ].map((o) => ({ ...o, value: (o.value !== '--') ? numberFormatter().format(o.value) : '--' }));

  const centerTableData = (el) => [
    { label: 'Perc_25', value: el?.medianMetrics?.perc25 ?? '--' },
    { label: 'Median', value: el?.medianMetrics?.median ?? '--' },
    { label: 'Perc_75', value: el?.medianMetrics?.perc75 ?? '--' },
  ].map((o) => ({ ...o, value: (o.value !== '--') ? numberFormatter().format(o.value) : '--' }));

  const rigthTableData = (el) => [
    { label: 'Miss_val', value: el?.missingValue?.count ?? '--' },
    { label: '%_miss_val', value: el?.missingValue?.percentage ?? '--' },
  ].map((o) => ({ ...o, value: (o.value !== '--') ? numberFormatter().format(o.value) : '--' }));

  return (
    <div className="flex flex-row gap-4">
      <DataTable
        columns={columns}
        dataSource={leftTableData(data)}
        modifier="basis-1/3"
        noHead
        pagination={false}
        rowClassName={DataTable.ROW_NOT_CLICKABLE}
        rowKey={({ label }) => label}
        size="small"
      />

      <DataTable
        columns={columns}
        dataSource={centerTableData(data)}
        modifier="basis-1/3"
        noHead
        pagination={false}
        rowClassName={DataTable.ROW_NOT_CLICKABLE}
        rowKey={({ label }) => label}
        size="small"
      />

      <DataTable
        columns={columns}
        dataSource={rigthTableData(data)}
        modifier="basis-1/3"
        noHead
        pagination={false}
        rowClassName={DataTable.ROW_NOT_CLICKABLE}
        rowKey={({ label }) => label}
        size="small"
      />
    </div>
  );
}

export default NumericalTable;
