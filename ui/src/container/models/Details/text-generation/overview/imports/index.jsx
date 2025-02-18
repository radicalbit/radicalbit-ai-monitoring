import SmartTable from '@Components/smart-table';
// @ts-ignore
import ImportCompletionButton from '@Components/ImportButton/import-completion-button';
import { NamespaceEnum } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { useGetCompletionImportsQueryWithPolling } from '@State/models/polling-hook';
import { Spin, Void } from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router';
import { getColumns } from './columns';

const { useGetCompletionImportsQuery } = modelsApiSlice;

export default function Imports() {
  useGetCompletionImportsQueryWithPolling();

  const { uuid } = useParams();

  const { data, isLoading } = useGetCompletionImportsQuery({ uuid });
  const importList = data?.items ?? [];

  if (isLoading) {
    return (<Spin spinning />);
  }

  if (importList.length === 0) {
    return (
      <Void
        actions={<ImportCompletionButton type="primary" />}
        description="Import a completion file to see the outcome"
        title="No completion data imported yet"
      />
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <FeedBackHeader />

      <FeedbackTable />
    </div>
  );
}

function FeedbackTable() {
  const { uuid: modelUUID } = useParams();

  const { data } = useGetCompletionImportsQuery({ uuid: modelUUID });
  const items = data?.items || [];
  const recordCount = data?.total;

  return (
    <SmartTable
      columns={getColumns}
      dataSource={items}
      modifier="w-full"
      namespace={NamespaceEnum.COMPLETION_IMPORT}
      recordCount={recordCount}
      rowKey={({ uuid }) => `${uuid}`}
    />

  );
}

function FeedBackHeader() {
  const { uuid } = useParams();

  const { data } = useGetCompletionImportsQuery({ uuid });
  const totalCounter = data?.total;

  return (
    <div className="flex items-center  p-4 justify-between">
      <div className="font-[var(--coo-font-weight-bold)]">
        {`${totalCounter} Dataset`}
      </div>

      <ImportCompletionButton />
    </div>
  );
}
