import {
  Json, NewHeader, RelativeDateTime, SectionTitle, StatusSelector,
} from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useParams, useSearchParams } from 'react-router-dom';

const { useGetSpanDetailByUUIDQuery } = tracingApiSlice;

function TraceDetail() {
  const { uuid: projectUuid } = useParams();

  const [searchParams] = useSearchParams();
  const traceUuid = searchParams.get('traceUuid');
  const spanId = searchParams.get('spanId');

  const { data } = useGetSpanDetailByUUIDQuery({ projectUuid, traceUuid, spanId }, { skip: !spanId });
  const name = data?.name;
  const createdAt = data?.createdAt;
  const duration = data?.durationsMs ? numberFormatter().format(data.durationsMs / 1000) : data?.durationsMs;
  const promptTokens = data?.promptTokens;
  const totalTokens = data?.totalTokens;
  const completionTokens = data?.completionTokens;
  const errorEvents = data?.errorEvents ?? [];

  const attributes = data?.attributes;

  const jsonData = attributes ? Object.entries(attributes).reduce((acc, [key, values]) => {
    try {
      return { ...acc, [key]: JSON.parse(values) };
    } catch (err) {
      return { ...acc, [key]: values };
    }
  }, {}) : '';

  return (
    <div className="flex flex-col w-full h-full">
      <NewHeader
        details={{
          one: <StatusSelector status={{ current: `${duration}s` }} title="Duration" />,
          two: <StatusSelector status={{ current: errorEvents.length }} title="Errors" />,
          three: <StatusSelector status={{ current: promptTokens }} title="Prompt tokens" />,
          four: <StatusSelector status={{ current: completionTokens }} title="Completion tokens" />,
          five: <StatusSelector status={{ current: totalTokens }} title="Total tokens" />,
        }}
        title={(
          <SectionTitle
            subtitle={<RelativeDateTime timestamp={createdAt} />}
            title={name}
          />
        )}
      />

      <Json data={jsonData} expandUntil={0} />

    </div>
  );
}

export default TraceDetail;
