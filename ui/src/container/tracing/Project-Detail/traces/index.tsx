import SmartTable from "@Components/smart-table";
import { NamespaceEnum } from "@Src/constants";
import { tracingApiSlice } from "@Src/store/state/tracing/api";
import { useParams } from "react-router";
import { useSearchParams } from "react-router-dom";
import { getColumns } from "./columns";
import TraceDetailDrawer from "./drawer";

const { useGetTracingProjectByUUIDQuery } = tracingApiSlice;

const TracesList = () => {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const { data } = useGetTracingProjectByUUIDQuery({ uuid });

  const items = data?.traceList ?? [];
  const count = data?.count;

  const handleOnClick = () => {
    searchParams.set("trace-detail", "true");
    setSearchParams(searchParams);
  };

  return (
    <div className="flex flex-col gap-2 pl-4">
      <span>ProjectSTraces</span>

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
      <TraceDetailDrawer></TraceDetailDrawer>
    </div>
  );
};

export default TracesList;
