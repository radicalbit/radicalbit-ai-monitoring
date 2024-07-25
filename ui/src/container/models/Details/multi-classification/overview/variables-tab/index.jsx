import { Button, DataTable } from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';
import { memo } from 'react';
import { modelsApiSlice } from '@Store/state/models/api';
import { OVERVIEW_ROW_TYPE } from '@Container/models/Details/constants';
import { FormbitContextProvider, useFormbitContext } from '@radicalbit/formbit';
import { JOB_STATUS } from '@Src/constants';
import { featuresColumns, featuresColumnsWithSelection } from './columns';
import useHandleOnSubmit from './useHandleOnSubmit';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function VariablesTab() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const features = data?.features ?? [];
  const target = data?.target;
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

  return (
    <FormbitContextProvider initialValues={{ __metadata: { variables } }}>
      <VariablesTabInner />
    </FormbitContextProvider>
  );
}

function VariablesTabInner() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });
  const { form } = useFormbitContext();

  const variables = form?.__metadata.variables ?? [];

  const referenceJobStatus = data?.latestReferenceJobStatus;
  const isMissingReference = referenceJobStatus === JOB_STATUS.MISSING_REFERENCE;
  const columns = (isMissingReference) ? featuresColumnsWithSelection(variables) : featuresColumns(variables);

  const handleRowClassName = ({ rowType }) => rowType.length > 0 ? DataTable.ROW_PRIMARY_LIGHT : '';

  const [handleOnSubmit, { isLoading }] = useHandleOnSubmit();
  return (
    <div className="flex flex-col mt-4">
      {isMissingReference && (
      <div className="flex justify-end">
        <Button
          loading={isLoading}
          onClick={handleOnSubmit}
          type="primary"
        >
          Update
        </Button>
      </div>
      )}

      <DataTable
        columns={columns}
        dataSource={variables.sort((a, b) => b.rowType.length - a.rowType.length)}
        pagination={{ pageSize: 20, hideOnSinglePage: true }}
        rowClassName={handleRowClassName}
        rowKey={({ name }) => name}
      />
    </div>
  );
}

export default memo(VariablesTab);
