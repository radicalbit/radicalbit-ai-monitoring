import SmartTable from "@Components/smart-table";
import { NamespaceEnum } from "@Src/constants";
import { tracingApiSlice } from "@Src/store/state/tracing/api";
import { useParams } from "react-router";
import { useSearchParams } from "react-router-dom";
import { getColumns } from "./columns";

const { useGetTracingProjectByUUIDQuery } = tracingApiSlice;

const SessionsList = () => {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const { data } = useGetTracingProjectByUUIDQuery({ uuid });

  const items = data?.traceList ?? [];
  const count = data?.count;

  const handleOnClick = (uuid) => {
    searchParams.set("sessionUuid", uuid);
    setSearchParams(searchParams);
  };

  return (
    <div className="flex flex-col gap-2 pl-4">
      <span>SessionsList</span>

      <SmartTable
        clickable
        columns={getColumns}
        dataSource={items}
        namespace={NamespaceEnum.SESSIONS_LIST}
        onRow={({ uuid }) => ({
          onClick: () => handleOnClick(uuid),
        })}
        recordCount={count}
        rowHoverable={false}
        rowKey={({ uuid }) => uuid}
      />
    </div>
  );
};

export default SessionsList;
