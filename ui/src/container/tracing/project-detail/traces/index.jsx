import SmartTable from '@Components/smart-table';
import { NamespaceEnum } from '@Src/constants';
import { selectors as contextConfigurationSelectors } from '@State/context-configuration';
import { tracingApiSlice } from '@State/tracing/api';
import { Spinner } from '@radicalbit/radicalbit-design-system';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import { getColumns } from './columns';
import TraceDetailDrawer from './drawer';
import Filters from './filters';
import externalFiltersToQueryParams from './filters/externalFiltersToQueryParams';

const { useGetTracesByProjectUUIDQuery } = tracingApiSlice;

function TracesList() {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const queryParams = useSelector((state) => contextConfigurationSelectors.selectQueryParamsSelector(state, NamespaceEnum.TRACES_LIST, externalFiltersToQueryParams));

  const { data, isLoading } = useGetTracesByProjectUUIDQuery({ uuid, queryParams });

  const items = data?.items ?? [];
  const count = data?.total;

  const modifier = items?.length ? '' : 'c-spinner--centered';

  const handleOnClick = () => {
    searchParams.set('trace-detail', 'true');
    setSearchParams(searchParams);
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
          onRow={({ uuid }) => ({
            onClick: () => handleOnClick(),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ uuid }) => uuid}
        />

        <TraceDetailDrawer />
      </div>

    </Spinner>
  );
}

export default TracesList;
