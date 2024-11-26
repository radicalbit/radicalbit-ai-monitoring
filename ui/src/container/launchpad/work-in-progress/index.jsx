import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import SmartTable from '@Components/smart-table';
import useModals from '@Hooks/use-modals';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { useGetModelQueryWithPolling } from '@State/models/polling-hook';
import {
  Button,
  NewHeader,
  SectionTitle,
  Void,
} from '@radicalbit/radicalbit-design-system';
import { useLocation, useNavigate } from 'react-router-dom';
import columns from './columns';
import getSkeletonColumns from './skeleton-columns';

function WorkInProgress() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const { data = [], isLoading, isError } = useGetModelQueryWithPolling();
  const models = data.items || [];
  const wipModels = models.filter(({ latestCurrentUuid, latestReferenceUuid }) => !latestCurrentUuid || !latestReferenceUuid);

  if (isError) {
    return (
      <div className="flex flex-col justify-start">
        <NewHeader
          title={<SectionTitle title="Models with no current" titleWeight="light" />}
        />

        <SomethingWentWrong size="small" />
      </div>
    );
  }

  if (wipModels.length === 0) {
    return (
      <div className="flex flex-col justify-start">
        <NewHeader
          title={<SectionTitle title="Models with no current" titleWeight="light" />}
        />

        <AddNewModelVoid />
      </div>
    );
  }

  return (
    <div className="flex flex-col justify-start">
      <NewHeader
        title={<SectionTitle title="Models with no current" titleWeight="light" />}
      />

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

function AddNewModelVoid() {
  const { showModal } = useModals();

  const handleOnAddModel = () => {
    showModal(ModalsEnum.ADD_NEW_MODEL);
  };

  return (
    <Void
      actions={<Button onClick={handleOnAddModel} type="default">New Model</Button>}
      description={(
        <>
          Define and configure a new model
          <br />
          to begin monitoring its performance and gain insights.
        </>
      )}
    />
  );
}

export default WorkInProgress;
