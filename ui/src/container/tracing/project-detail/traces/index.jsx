import SmartTable from '@Components/smart-table';
<<<<<<< HEAD
import { Spinner } from '@radicalbit/radicalbit-design-system';
import { ModalsEnum, NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { tracingApiSlice } from '@State/tracing/api';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import useModals from '@Hooks/use-modals';
import { getColumns } from './columns';
=======
import { NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { tracingApiSlice } from '@State/tracing/api';
import { Spinner } from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { getColumns } from './columns';
import TraceDetailDrawer from './drawer';
>>>>>>> main
import Filters from './filters';
import externalFiltersToQueryParams from './filters/externalFiltersToQueryParams';

const { useGetTracesByProjectUUIDQuery } = tracingApiSlice;

function TracesList() {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
<<<<<<< HEAD
  const { showModal } = useModals();
=======
>>>>>>> main

  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.TRACES_LIST, externalFiltersToQueryParams));

  const { data, isLoading } = useGetTracesByProjectUUIDQuery({ uuid, queryParams });

  const items = data?.items ?? [];
  const count = data?.total;

  const modifier = items?.length ? '' : 'c-spinner--centered';

<<<<<<< HEAD
  const handleOnClick = (traceUuid) => {
    searchParams.set('traceUuid', traceUuid);
    setSearchParams(searchParams);
    showModal(ModalsEnum.TRACE_DETAIL);
=======
  const handleOnClick = () => {
    searchParams.set('trace-detail', 'true');
    setSearchParams(searchParams);
>>>>>>> main
  };

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
<<<<<<< HEAD
=======

>>>>>>> main
      <div className="flex flex-col gap-2">
        <Filters />

        <SmartTable
          clickable
          columns={getColumns}
          dataSource={items}
          namespace={NamespaceEnum.TRACES_LIST}
<<<<<<< HEAD
          onRow={({ traceId }) => ({
            onClick: () => handleOnClick(traceId),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ traceId }) => traceId}
        />
      </div>
=======
          onRow={({ uuid }) => ({
            onClick: () => handleOnClick(),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ uuid }) => uuid}
        />

        <TraceDetailDrawer />
      </div>

>>>>>>> main
    </Spinner>
  );
}

export default TracesList;
