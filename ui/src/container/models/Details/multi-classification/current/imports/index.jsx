import ImportCurrentDatasetButton from '@Components/ImportButton/import-current-button';
import SmartTable from '@Components/smart-table';
import { NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { modelsApiSlice } from '@State/models/api';
import { useGetCurrentImportsQueryWithPolling } from '@State/models/polling-hook';
import { Spin, Void } from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import { getColumns } from './columns';

const { useGetCurrentImportsQuery } = modelsApiSlice;

export default function Imports() {
  useGetCurrentImportsQueryWithPolling();

  const { uuid } = useParams();
  const { data, isLoading } = useGetCurrentImportsQuery({ uuid });
  const importList = data?.items ?? [];

  if (isLoading) {
    return (<Spin spinning />);
  }

  if (importList.length === 0) {
    return (

      <Void
        actions={(<ImportCurrentDatasetButton type="primary" />)}
        description={(
          <>
            Ther is no data available
            <br />

            {'Import a dataset or with Python following these '}

            <strong>instructions</strong>
          </>
          )}
        title="No current dataset imported yet"
      />
    );
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      <FeedBackHeader />

      <FeedbackTable />
    </div>
  );
}

function FeedbackTable() {
  const { uuid: modelUUID } = useParams();
  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.CURRENT_IMPORT));

  const { data } = useGetCurrentImportsQuery({ uuid: modelUUID, queryParams });
  const items = data?.items || [];
  const recordCount = data?.total;

  return (
    <SmartTable
      columns={getColumns}
      dataSource={items}
      modifier="w-full pt-4"
      namespace={NamespaceEnum.CURRENT_IMPORT}
      recordCount={recordCount}
      rowKey={({ uuid }) => `${uuid}`}
    />

  );
}

function FeedBackHeader() {
  const { uuid } = useParams();

  const { data } = useGetCurrentImportsQuery({ uuid });
  const totalCounter = data?.total;

  return (
    <div className="flex items-center justify-between">
      <div className="font-[var(--coo-font-weight-bold)]">
        {`${totalCounter} Dataset`}
      </div>

      <ImportCurrentDatasetButton />
    </div>
  );
}
