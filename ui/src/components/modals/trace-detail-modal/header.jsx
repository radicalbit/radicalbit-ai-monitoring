import { faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import useModals from '@Hooks/use-modals';
import {
  FontAwesomeIcon, NewHeader, RelativeDateTime, SectionTitle, StatusSelector,
} from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { useParams } from 'react-router';
import { useSearchParams } from 'react-router-dom';

const { useGetTraceDetailByUUIDQuery } = tracingApiSlice;

function Header() {
  const { uuid: projectUuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const { hideModal } = useModals();

  const traceUuid = searchParams.get('traceUuid');

  const { data: traceData } = useGetTraceDetailByUUIDQuery({ projectUuid, traceUuid });
  const spansCounter = traceData?.spans;
  const duration = traceData?.durationMs ? numberFormatter().format(traceData.durationMs / 1000) : traceData?.durationMs;
  const totalTokens = traceData?.totalTokens;
  const completionTokens = traceData?.completionTokens;
  const promptTokens = traceData?.promptTokens;
  const numberOfErrors = traceData?.numberOfErrors;
  const createdAt = traceData?.createdAt;

  const handleOnCancel = () => {
    searchParams.delete('traceUuid');
    searchParams.delete('spanId');
    searchParams.delete('expandedKey');
    setSearchParams(searchParams);
    hideModal();
  };

  return (
    <NewHeader
      details={{
        one: <StatusSelector status={{ current: `${duration}s` }} title="Duration" />,
        two: <StatusSelector status={{ current: spansCounter }} title="Spans" />,
        three: <StatusSelector status={{ current: numberOfErrors }} title="Errors" />,
        four: (
          <>
            <StatusSelector status={{ current: completionTokens }} title="Completion tokens" />

            <StatusSelector status={{ current: promptTokens }} title="Prompt tokens" />

            <StatusSelector status={{ current: totalTokens }} title="Total tokens" />

          </>
        ),

      }}
      prefix={<FontAwesomeIcon enableColorMode icon={faArrowLeft} onClick={handleOnCancel} />}
      title={(
        <SectionTitle
          subtitle={<RelativeDateTime timestamp={createdAt} />}
          title={traceUuid}
        />
        )}
    />
  );
}
export default Header;
