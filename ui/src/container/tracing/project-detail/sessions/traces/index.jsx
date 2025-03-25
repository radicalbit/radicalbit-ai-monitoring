import SmartTable from '@Components/smart-table';
import { Spinner } from '@radicalbit/radicalbit-design-system';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { tracingApiSlice } from '@State/tracing/api';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import useModals from '@Hooks/use-modals';
import { getColumns } from './columns';
import Filters from './filters';
import externalFiltersToQueryParams from './filters/externalFiltersToQueryParams';

const { useGetTracesByProjectUUIDQuery } = tracingApiSlice;

function SessionsTracesList() {
  const { showModal } = useModals();
  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.SESSION_TRACES, externalFiltersToQueryParams));

  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const { data, isLoading, isFetching } = useGetTracesByProjectUUIDQuery({ uuid, queryParams }, { skip: !queryParams.includes('sessionUuid') });
  const items = data?.items ?? [];
  const count = data?.total;

  const handleOnClick = (traceUuid) => {
    searchParams.set('traceUuid', traceUuid);
    setSearchParams(searchParams);
    showModal(ModalsEnum.TRACE_DETAIL);
  };

  const modifier = items?.length ? '' : 'c-spinner--centered';

  return (
    <div className="flex flex-col gap-2">
      <Filters />

      <Spinner fullHeight modifier={modifier} spinning={isLoading || isFetching}>

        <SmartTable
          clickable
          columns={getColumns}
          dataSource={items}
          namespace={NamespaceEnum.SESSION_TRACES}
          onRow={({ traceId }) => ({
            onClick: () => handleOnClick(traceId),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ traceId }) => traceId}
        />
      </Spinner>
    </div>
  );
}

export default SessionsTracesList;
