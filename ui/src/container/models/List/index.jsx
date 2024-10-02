import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import SmartTable from '@Components/smart-table';
import LogoSquared from '@Img/logo-collapsed.svg';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import { useGetModelQueryWithPolling } from '@Src/store/state/models/polling-hook';
import { Button, Spinner, Void } from '@radicalbit/radicalbit-design-system';
import { useLocation, useNavigate } from 'react-router-dom';
import { getColumns } from './columns';

export function ModelsList() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const { data, isLoading, isError } = useGetModelQueryWithPolling();

  const models = data?.items || [];
  const count = data?.total || 0;

  // TODO we use the following object only for mock purpose. Must be removed when BE are ready
  const modelsWithMock = models.map(((m) => ({
    ...m,
    dataQuality: { current: null, reference: null },
    modelQuality: { current: null, reference: null },
    dataDrift: { current: null, reference: null },
  })));

  const modifier = models?.length ? '' : 'c-spinner--centered';

  if (isError) {
    return <SomethingWentWrong />;
  }

  return (
    <Spinner
      fullHeight
      hideChildren
      modifier={modifier}
      spinning={isLoading}
    >
      {!models.length && (
        <Void
          actions={<AddNewModel />}
          description="No models are available."
          image={<LogoSquared />}
          title="Empty Models list"
        />
      )}

      {!!models.length && (
        <SmartTable
          clickable
          columns={getColumns}
          dataSource={modelsWithMock}
          namespace={NamespaceEnum.MODELS}
          onRow={({ uuid }) => ({
            onClick: () => navigate({
              pathname: `${uuid}`,
              search,
            }),
          })}
          recordCount={count}
          rowKey={({ uuid }) => uuid}
        />
      )}
    </Spinner>
  );
}

function AddNewModel() {
  const { showModal } = useModals();

  const onClick = () => {
    showModal(ModalsEnum.ADD_NEW_MODEL);
  };

  return (
    <Button onClick={onClick} type="primary">
      New Model
    </Button>
  );
}
