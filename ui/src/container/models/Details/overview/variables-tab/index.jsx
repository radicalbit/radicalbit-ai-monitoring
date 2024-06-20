import { DataTable } from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';
import { memo } from 'react';
import { modelsApiSlice } from '@Store/state/models/api';
import featuresColumns from './columns';
import { OVERVIEW_ROW_TYPE } from '../../constants';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function VariablesTab() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const features = data?.features ?? [];
  const target = data?.target ?? [];
  const variables = [target].concat(features).map((f) => ({
    ...f,
    rowType: f.name === target.name ? OVERVIEW_ROW_TYPE.GROUND_TRUTH : '',
  }));

  const handleRowClassName = ({ rowType }) => rowType.length > 0 ? DataTable.ROW_PRIMARY_LIGHT : '';

  return (
    <DataTable
      columns={featuresColumns(variables)}
      dataSource={variables.sort((a, b) => b.rowType.length - a.rowType.length)}
      pagination={{ pageSize: 200, hideOnSinglePage: true }}
      rowClassName={handleRowClassName}
      rowKey={({ name }) => name}
    />
  );
}

export default memo(VariablesTab);
