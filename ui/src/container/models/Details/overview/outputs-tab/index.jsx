import { DataTable } from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { useParams } from 'react-router';
import { modelsApiSlice } from '@Store/state/models/api';
import { OVERVIEW_ROW_TYPE } from '../../constants';
import outputsColumns from './columns';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function OutputsTab() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const predictionProba = data?.outputs.predictionProba;
  const prediction = data?.outputs.prediction;

  const outputs = data?.outputs.output.map((output) => {
    const rowOutputType = (function getRowType({ name }) {
      if (name === predictionProba?.name) {
        return OVERVIEW_ROW_TYPE.PROBABILITY;
      }

      if (name === prediction.name) {
        return OVERVIEW_ROW_TYPE.PREDICTION;
      }

      return '';
    }(output));

    return { ...output, outputType: rowOutputType };
  }) ?? [];

  const handleRowClassName = ({ name }) => (name === predictionProba?.name) || (name === prediction.name) ? DataTable.ROW_PRIMARY_LIGHT : '';

  return (
    <DataTable
      columns={outputsColumns(outputs)}
      dataSource={outputs.sort((a, b) => b.outputType.length - a.outputType.length)}
      pagination={{ pageSize: 200, hideOnSinglePage: true }}
      rowClassName={handleRowClassName}
      rowKey={({ name }) => name}
    />
  );
}

export default memo(OutputsTab);
