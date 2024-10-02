import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { useGetModelQueryWithPolling } from '@State/models/polling-hook';
import { Board, DataTable, Skeleton } from '@radicalbit/radicalbit-design-system';
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
        header="Work in progress"
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
        header="Work in progress"
        main={<SomethingWentWrong size="small" />}
      />
    );
  }

  return (
    <Board
      header="Work in progress"
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
    />
  );
}

export default WorkInProgress;
