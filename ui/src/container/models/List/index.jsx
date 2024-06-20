import SmartTable from '@Components/smart-table';
import LogoSquared from '@Img/logo-collapsed.svg';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import useModals from '@Src/hooks/use-modals';
import { modelsApiSlice } from '@Src/store/state/models/api';
import { Button, Spinner, Void } from '@radicalbit/radicalbit-design-system';
import { useLocation, useNavigate } from 'react-router-dom';
import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import { useSelector } from 'react-redux';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { getColumns } from './columns';

const { useGetModelsQuery } = modelsApiSlice;

const { selectQueryParamsSelector } = contextConfigurationSelectors;

export function ModelsList() {
  const navigate = useNavigate();
  const { search } = useLocation();

  const queryParams = useSelector((state) => selectQueryParamsSelector(state, NamespaceEnum.MODELS));

  const { data, isLoading, isError } = useGetModelsQuery({ queryParams });

  const models = data?.items || [];
  const count = data?.total || 0;

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
