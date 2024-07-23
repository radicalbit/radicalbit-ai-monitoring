import { DataTable } from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';
import { memo } from 'react';
import { modelsApiSlice } from '@Store/state/models/api';
import { OVERVIEW_ROW_TYPE } from '@Container/models/Details/constants';
import featuresColumns from './columns';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function VariablesTab() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const features = data?.features ?? [];
  const target = data?.target ?? [];
  const timestamp = data?.timestamp;
  const variables = [target, timestamp].concat(features).map((f) => ({
    ...f,
    rowType: (function getLabel() {
      switch (f.name) {
        case target.name:
          return OVERVIEW_ROW_TYPE.GROUND_TRUTH;
        case timestamp.name:
          return OVERVIEW_ROW_TYPE.TIMESTAMP;
        default:
          return '';
      }
    }()),

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
