import SessionLatenciesTable from "@Container/tracing/project-detail/dashboard/session-latencies-table"
import SpanLatenciesTable from "@Container/tracing/project-detail/dashboard/span-latencies-table"
import TraceLatenciesTable from "@Container/tracing/project-detail/dashboard/trace-latencies-table"
import { Board } from "@radicalbit/radicalbit-design-system"

function ProjectDashboard() {
    return (
        <div className="flex flex-col gap-4">
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
        </div>
    )
}

export default ProjectDashboard