import SmartTable from '@Components/smart-table';
// @ts-ignore
import ImportReferenceButton from '@Components/ImportButton/import-reference-button';
import LogoSquared from '@Img/logo-collapsed.svg';
import { modelsApiSlice } from '@State/models/api';
import { useGetReferenceImportsQueryWithPolling } from '@State/models/polling-hook';
import { Spin, Void } from '@radicalbit/radicalbit-design-system';
import { useParams } from 'react-router-dom';
import { NamespaceEnum } from '@Src/constants';
import { getColumns } from './columns';

const { useGetReferenceImportsQuery } = modelsApiSlice;

export default function Imports() {
  useGetReferenceImportsQueryWithPolling();

  const { uuid } = useParams();

  const { data, isLoading } = useGetReferenceImportsQuery({ uuid });
  const importList = data?.items ?? [];

  if (isLoading) {
    return (<Spin spinning />);
  }

  if (importList.length === 0) {
    return (
      <Void
        actions={<ImportReferenceButton type="primary" />}
        description="Import a reference file to see the outcome"
        image={<LogoSquared />}
        title="No reference data imported yet"
      />
    );
  }

  return (
    <FeedbackTable />
  );
}

function FeedbackTable() {
  const { uuid: modelUUID } = useParams();

  const { data } = useGetReferenceImportsQuery({ uuid: modelUUID });
  const items = data?.items || [];
  const recordCount = data?.total;

  return (
    <SmartTable
      columns={getColumns}
      dataSource={items}
      modifier="w-full pt-4"
      namespace={NamespaceEnum.REFERENCE_IMPORT}
      recordCount={recordCount}
      rowKey={({ uuid }) => `${uuid}`}
    />

  );
}
