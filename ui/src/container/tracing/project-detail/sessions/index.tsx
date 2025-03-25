import SmartTable from "@Components/smart-table";
import LogoSquared from "@Img/logo-collapsed.svg";
import { Button, Spinner, Void } from "@radicalbit/radicalbit-design-system";
import { NamespaceEnum } from "@Src/constants";
import { tracingApiSlice } from "@State/tracing/api";
import { useParams } from "react-router";
import { useSearchParams } from "react-router-dom";
import getSessionColumns from "./get-session-columns";

const { useGetSessionsByProjectUUIDQuery } = tracingApiSlice;

const SessionsList = () => {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();

  const { data, isLoading } = useGetSessionsByProjectUUIDQuery({ uuid });
  const items = data?.items ?? [];
  const count = data?.total;

  const handleOnClick = (uuid) => {
    searchParams.set("sessionUuid", uuid);
    setSearchParams(searchParams);
  };

  const modifier = items?.length ? "" : "c-spinner--centered";

  return (
    <Spinner fullHeight hideChildren modifier={modifier} spinning={isLoading}>
      {!items.length && (
        <Void
          image={<LogoSquared />}
          title="No traces available"
          description="copy description needed"
          actions={<Button type="primary">Copy for CTA</Button>}
        />
      )}

      {!!items.length && (
        <SmartTable
          clickable
          columns={getSessionColumns}
          dataSource={items}
          namespace={NamespaceEnum.SESSIONS_LIST}
          onRow={({ uuid }) => ({
            onClick: () => handleOnClick(uuid),
          })}
          recordCount={count}
          rowHoverable={false}
          rowKey={({ uuid }) => uuid}
        />
      )}
    </Spinner>
  );
};

export default SessionsList;
