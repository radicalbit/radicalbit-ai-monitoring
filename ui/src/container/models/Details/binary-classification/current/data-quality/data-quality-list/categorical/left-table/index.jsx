import { DataTable } from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import columns from './columns';

function CategoricalLeftTable({ data }) {
  const dataSource = (el) => [
    { label: 'Missing values', value: el.missingValue.count },
    { label: 'Missing values %', value: el.missingValue.percentage },
    { label: 'Distinct values', value: el?.distinctValue ?? '--' },
  ].map((o) => ({ ...o, value: (o.value !== '--') ? numberFormatter().format(o.value) : '--' }));

  return (
    <DataTable
      columns={columns}
      dataSource={dataSource(data)}
      noHead
      pagination={false}
      rowClassName={DataTable.ROW_NOT_CLICKABLE}
      rowHoverable={false}
      rowKey={({ label }) => label}
      size="small"
    />
  );
}

export default CategoricalLeftTable;
