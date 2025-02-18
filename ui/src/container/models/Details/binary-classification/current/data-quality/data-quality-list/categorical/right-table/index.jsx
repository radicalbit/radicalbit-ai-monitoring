import { DataTable } from '@radicalbit/radicalbit-design-system';
import columns from './columns';

function CategoricalRightTable({ data }) {
  if (!data) {
    return false;
  }

  return (
    <DataTable
      columns={columns}
      dataSource={data}
      modifier="w-full"
      pagination={false}
      rowClassName={() => DataTable.ROW_NOT_CLICKABLE}
      rowHoverable={false}
      rowKey={({ name }) => name}
      scroll={{ y: '12rem' }}
      size="small"
    />
  );
}

export default CategoricalRightTable;
