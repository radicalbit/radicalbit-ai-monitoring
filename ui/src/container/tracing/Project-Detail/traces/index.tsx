import SmartTable from "@Components/smart-table";
import { NamespaceEnum } from "@Src/constants";
import { tracingApiSlice } from "@Src/store/state/tracing/api";
import { useParams } from "react-router";
import { useSearchParams } from "react-router-dom";
import { getColumns } from "./columns";
import TraceDetailDrawer from "./drawer";
import { Button, Spinner, Void } from "@radicalbit/radicalbit-design-system";
import LogoSquared from "@Img/logo-collapsed.svg";

const { useGetProjectByUUIDQuery } = tracingApiSlice;

const TracesList = () => {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const { data, isLoading, isError } = useGetProjectByUUIDQuery({ uuid });

  const items = data?.traces ?? [];
  const count = data?.count;

  const modifier = items?.length ? "" : "c-spinner--centered";

  const handleOnClick = () => {
    searchParams.set("trace-detail", "true");
    setSearchParams(searchParams);
  };

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
      {!items.length && (
        <Void
          image={<LogoSquared />}
          title="No traces available"
          description="copy description needed"
          actions={<Button  type="primary" >Copy for CTA</Button>}
        />
      )}

      {!!items.length && (
        <>
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
        </>
      )}
    </Spinner>
  );
};

export default TracesList;
