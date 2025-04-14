import SessionLatenciesTable from '@Container/tracing/project-detail/dashboard/session-latencies-table';
import SpanLatenciesTable from '@Container/tracing/project-detail/dashboard/span-latencies-table';
import TraceLatenciesTable from '@Container/tracing/project-detail/dashboard/trace-latencies-table';
import { FormbitContextProvider } from '@radicalbit/formbit';
import { Board } from '@radicalbit/radicalbit-design-system';
import dayjs from 'dayjs';
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
        <Filters />

        <div className="flex flex-col gap-2">
          <Board
            header={<h2>Trace latencies</h2>}
            main={<TraceLatenciesTable />}
          />

          <Board
            header={<h2>Session latencies</h2>}
            main={<SessionLatenciesTable />}
          />

          <Board
            header={<h2>Span latencies</h2>}
            main={<SpanLatenciesTable />}
          />

          <TraceByTimeLineChart />

          <TracesBySessionHistogram />
        </div>
      </div>
    </FormbitContextProvider>
  );
}

export default ProjectDashboard;
