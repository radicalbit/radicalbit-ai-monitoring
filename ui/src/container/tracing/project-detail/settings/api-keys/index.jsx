import SmartTable from '@Components/smart-table';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import LogoSquared from '@Img/logo-collapsed.svg';
import {
  Alert,
  Board, Button,
  CopyToClipboard,
  FontAwesomeIcon, SectionTitle, Spinner, Void,
} from '@radicalbit/radicalbit-design-system';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { useParams } from 'react-router';
import useModals from '@Hooks/use-modals';
import { useSelector } from 'react-redux';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import getApiKeyColumns from './get-api-keys-column';

const { useGetApiKeyListQuery, useAddNewApiKeyMutation, useAddNewProjectMutation } = tracingApiSlice;

function ApiKeysProject() {
  return (
    <Board
      header={(
        <div className="flex flex-row justify-between items-end">
          <SectionTitle
            size="large"
            title="Api keys"
            titleColor="primary"
          />

          <ApiKeyCreateButtonIcon />
        </div>
          )}
      main={(<ApiKeysList />)}
    />
  );
}

function ApiKeysList() {
  const { uuid } = useParams();

  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.API_KEYS_LIST));

  const { data, isLoading } = useGetApiKeyListQuery({ uuid, queryParams });
  const items = data?.items ?? [];
  const count = data?.total;

  const modifier = items?.length ? '' : 'c-spinner--centered';

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
      {!items.length && (
        <Void
          actions={<ApiKeyCreateButton />}
          description="copy description needed"
          image={<LogoSquared />}
          title="No traces available"
        />
      )}

      {!!items.length && (
        <>
          <CopyNewApiKey />

          <SmartTable
            clickable
            columns={getApiKeyColumns}
            dataSource={items}
            namespace={NamespaceEnum.API_KEYS_LIST}
            recordCount={count}
            rowHoverable={false}
            rowKey={({ sessionUuid }) => sessionUuid}
          />
        </>
      )}
    </Spinner>
  );
}

function ApiKeyCreateButton() {
  const { uuid } = useParams();
  const { showModal } = useModals();

  const handleOnClick = () => {
    showModal(ModalsEnum.ADD_NEW_API_KEY, { uuid });
  };

  return (
    <Button onClick={handleOnClick}>Add key</Button>
  );
}

function ApiKeyCreateButtonIcon() {
  const { uuid } = useParams();
  const { showModal } = useModals();

  const handleOnClick = () => {
    showModal(ModalsEnum.ADD_NEW_API_KEY, { uuid });
  };

  return (
    <Button onClick={handleOnClick} shape="circle" title="Add new keys">
      <FontAwesomeIcon icon={faPlus} />
    </Button>
  );
}

function CopyNewApiKey() {
  const [, addNewProjectArgs] = useAddNewProjectMutation({ fixedCacheKey: 'add-new-project' });
  const [, addNewApiKeyArgs] = useAddNewApiKeyMutation({ fixedCacheKey: 'add-new-api-key' });
  const apiKey = addNewProjectArgs?.data?.apiKey?.apiKey || addNewApiKeyArgs.data?.apiKey;

  if (!apiKey) {
    return false;
  }

  return (
    <Alert
      closable
      description={(
        <div className="flex flex-col items-center gap-2">
          New key added

          <small>Remeber: this key can only be viewed once.</small>

          <div className="flex flex-row justify-center gap-2">

            <strong>{apiKey}</strong>

            <CopyToClipboard link={apiKey} />

          </div>

        </div>
      )}
      type="success"
    />

  );
}

export default ApiKeysProject;
