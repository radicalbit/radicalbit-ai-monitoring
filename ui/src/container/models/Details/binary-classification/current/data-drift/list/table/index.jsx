import { DataTable } from '@radicalbit/radicalbit-design-system';
import columns from './columns';

function DetailDriftTable({ data }) {
  if (!data) {
    return false;
  }

  return (
    <DataTable
      columns={columns}
      dataSource={data}
      pagination={false}
      rowClassName={DataTable.ROW_NOT_CLICKABLE}
      rowHoverable={false}
      rowKey={({ label }) => label}
      size="small"
    />

  );
}

export default DetailDriftTable;
