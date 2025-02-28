import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import SmartTable from '@Components/smart-table';
import { NamespaceEnum } from '@Src/constants';
import { useGetModelsQueryWithPolling } from '@State/models/polling-hook';
import {
  NewHeader,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useLocation, useNavigate } from 'react-router-dom';
import columns from './columns';
import getSkeletonColumns from './skeleton-columns';

function WorkInProgress() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const { data = [], isLoading, isError } = useGetModelsQueryWithPolling();
  const models = data.items || [];
  const wipModels = models.filter(({ latestCurrentUuid, latestReferenceUuid }) => !latestCurrentUuid || !latestReferenceUuid);

  if (isError) {
    return (
      <div className="flex flex-col justify-start">
        <NewHeader title={<SectionTitle title="Models with no current" titleWeight="light" />} />

        <SomethingWentWrong size="small" />
      </div>
    );
  }

  if (wipModels.length === 0) {
    return false;
  }

  return (
    <div className="flex flex-col justify-start">
      <NewHeader title={<SectionTitle title="Models with no current" titleWeight="light" />} />

      <SmartTable
        clickable
        columns={isLoading ? getSkeletonColumns : columns}
        dataSource={wipModels}
        fixedHeader="30rem"
        namespace={NamespaceEnum.MODELS_STATS}
        onRow={({ uuid }) => ({
          onClick: () => navigate({ pathname: `/models/${uuid}`, search }),
        })}
        pagination={false}
        rowKey={({ uuid }) => uuid}
        size="small"
      />
    </div>
  );
}

export default WorkInProgress;
