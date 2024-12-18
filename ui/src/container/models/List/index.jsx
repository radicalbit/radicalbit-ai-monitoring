import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { useInitDarkMode } from '@Components/dark-mode/hooks';
import SmartTable from '@Components/smart-table';
import { MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import LogoSquared from '@Img/logo-collapsed.svg';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import { useGetModelsQueryWithPolling } from '@State/models/polling-hook';
import { Button, Spinner, Void } from '@radicalbit/radicalbit-design-system';
import { useLocation, useNavigate } from 'react-router-dom';
import { getColumns } from './columns';

export function ModelsList() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const { data, isLoading, isError } = useGetModelsQueryWithPolling();
  const models = data?.items || [];
  const count = data?.total || 0;

  useInitDarkMode(MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION);

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
          dataSource={models}
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
