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

function TracesList() {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const { showModal } = useModals();

  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.TRACES_LIST, externalFiltersToQueryParams));

  const { data, isLoading } = useGetTracesByProjectUUIDQuery({ uuid, queryParams });

  const items = data?.items ?? [];
  const count = data?.total;

  const modifier = items?.length ? '' : 'c-spinner--centered';

  const handleOnClick = (traceUuid) => {
    searchParams.set('traceUuid', traceUuid);
    setSearchParams(searchParams);
    showModal(ModalsEnum.TRACE_DETAIL);
  };

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
      <div className="flex flex-col gap-2">
        <Filters />

        <SmartTable
          clickable
          columns={getColumns}
          dataSource={items}
          namespace={NamespaceEnum.TRACES_LIST}
          onRow={({ traceId }) => ({
            onClick: () => handleOnClick(traceId),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ traceId }) => traceId}
        />
      </div>
    </Spinner>
  );
}

export default TracesList;
