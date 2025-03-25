import SmartTable from '@Components/smart-table';
import LogoSquared from '@Img/logo-collapsed.svg';
import { Button, Spinner, Void } from '@radicalbit/radicalbit-design-system';
import { NamespaceEnum } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { useSelector } from 'react-redux';
import getSessionColumns from './get-session-columns';

const { useGetSessionsByProjectUUIDQuery } = tracingApiSlice;

function SessionsList() {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.SESSIONS_LIST));

  const { data, isLoading } = useGetSessionsByProjectUUIDQuery({ uuid, queryParams });
  const items = data?.items ?? [];
  const count = data?.total;

  const handleOnClick = (sessionUuid) => {
    searchParams.set('sessionUuid', sessionUuid);
    setSearchParams(searchParams);
  };

  const modifier = items?.length ? '' : 'c-spinner--centered';

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
      {!items.length && (
        <Void
          actions={<Button type="primary">Copy for CTA</Button>}
          description="copy description needed"
          image={<LogoSquared />}
          title="No traces available"
        />
      )}

      {!!items.length && (
        <SmartTable
          clickable
          columns={getSessionColumns}
          dataSource={items}
          namespace={NamespaceEnum.SESSIONS_LIST}
          onRow={({ sessionUuid }) => ({
            onClick: () => handleOnClick(sessionUuid),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ sessionUuid }) => sessionUuid}
        />
      )}
    </Spinner>
  );
}

export default SessionsList;
