import SessionLatenciesTable from '@Container/tracing/project-detail/dashboard/session-latencies-table';
import SpanLatenciesTable from '@Container/tracing/project-detail/dashboard/span-latencies-table';
import TraceLatenciesTable from '@Container/tracing/project-detail/dashboard/trace-latencies-table';
import { FormbitContextProvider } from '@radicalbit/formbit';
import { Board, SectionTitle, Tabs } from '@radicalbit/radicalbit-design-system';
import dayjs from 'dayjs';
import { useSearchParams } from 'react-router-dom';
import Filters from './filters';
import schema from './schema';
import TraceByTimeLineChart from './trace-by-time-line-chart';
import TracesBySessionHistogram from './traces-by-session-histogram';

const initialValues = {
  fromTimestamp: dayjs().subtract(24, 'hour').toISOString(),
  toTimestamp: dayjs().toISOString(),
};

function ProjectDashboard() {
  return (
    <FormbitContextProvider initialValues={initialValues} schema={schema}>
      <div className="flex flex-col gap-4 p-4">
        <div className="flex justify-end">
          <Filters />
        </div>

        <div className="flex flex-col gap-8 ">
          <div className="flex flex-col gap-4">
            <TraceByTimeLineChart />

            <Board
              header={<SectionTitle title="Trace latencies" />}
              main={<TraceLatenciesTable />}
            />
          </div>

          <DashboardTabs />
        </div>
      </div>
    </FormbitContextProvider>
  );
}

function DashboardTabs() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get('section') || 'session';

  const handleOnChangeTabs = (tab) => {
    searchParams.set('section', tab);
    setSearchParams(searchParams);
  };

  return (
    <Tabs
      activeKey={activeTab}
      items={[
        {
          label: 'Session',
          key: 'session',
          children: (
            <div className="flex flex-col gap-4">
              <Board
                header={<SectionTitle title="Session latencies" />}
                main={<SessionLatenciesTable />}
              />

              <TracesBySessionHistogram />
            </div>),
        },
        {
          label: 'Span',
          key: 'span',
          children: <Board
            header={<SectionTitle title="Span latencies" />}
            main={<SpanLatenciesTable />}
          />,
        },
      ]}
      modifier="h-[96%]"
      noBorder
      onChange={handleOnChangeTabs}
    />
  );
}

export default ProjectDashboard;
