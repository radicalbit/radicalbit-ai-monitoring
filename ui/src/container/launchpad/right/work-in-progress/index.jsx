import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import useModals from '@Hooks/use-modals';
import { ModalsEnum } from '@Src/constants';
import { useGetModelQueryWithPolling } from '@State/models/polling-hook';
import {
  Board, Button, DataTable, SectionTitle, Skeleton, Void,
} from '@radicalbit/radicalbit-design-system';
import { useLocation, useNavigate } from 'react-router-dom';
import columns from './columns';

function WorkInProgress() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const { data = [], isLoading, isError } = useGetModelQueryWithPolling();
  const models = data.items || [];
  const wipModels = models.filter(({ latestCurrentUuid, latestReferenceUuid }) => !latestCurrentUuid || !latestReferenceUuid);

  if (isLoading) {
    return (
      <Board
        header={<SectionTitle size="small" title="Work in progress" />}
        main={(
          <div className="flex flex-col gap-2">
            <Skeleton.Input active block />

            <Skeleton.Input active block />

            <Skeleton.Input active block />
          </div>
      )}
      />
    );
  }

  if (isError) {
    return (
      <Board
        header={<SectionTitle size="small" title="Work in progress" />}
        main={<SomethingWentWrong size="small" />}
        size="small"
      />
    );
  }

  if (wipModels.length === 0) {
    return (
      <Board
        header={<SectionTitle size="small" title="Work in progress" />}
        height="250px"
        main={(<AddNewModelVoid />)}
        size="small"
      />
    );
  }

  return (
    <Board
      header={<SectionTitle size="small" title="Work in progress" />}
      height="300px"
      main={(
        <DataTable
          clickable
          columns={columns}
          dataSource={wipModels}
          onRow={({ uuid }) => ({
            onClick: () => navigate({ pathname: `/models/${uuid}`, search }),
          })}
          pagination={false}
          rowKey={({ uuid }) => uuid}
          scroll={{ y: '16rem' }}
          size="small"
        />
      )}
      size="small"
    />
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
