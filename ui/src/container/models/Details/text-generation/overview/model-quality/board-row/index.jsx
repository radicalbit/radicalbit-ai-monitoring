import { Board, SectionTitle } from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import { useGetCompletionModelQualityQueryWithPolling } from '@Src/store/state/models/polling-hook';

function BoardRow() {
  return (
    <div className="flex flex-row gap-4 w-full h-[15rem]">
      <div className="w-1/3">
        <ObjectCounter />
      </div>

      <div className="w-1/3">
        <GlobalPerplexityBoard />
      </div>

      <div className="w-1/3">
        <GlobalProbabilityBoard />
      </div>

    </div>
  );
}

function ObjectCounter() {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const counter = data?.modelQuality?.tokens.length ?? 0;

  return (
    <Board
      header={<SectionTitle size="small" title="Number of sentences" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{counter}</div>
          </div>

        </div>
      )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

function GlobalPerplexityBoard() {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const counter = data?.modelQuality?.meanPerFile[0].perplexTotMean ?? 0;

  return (
    <Board
      header={<SectionTitle size="small" title="Perplexity overall" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{numberFormatter().format(counter)}</div>
          </div>

        </div>
        )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

function GlobalProbabilityBoard() {
  const { data } = useGetCompletionModelQualityQueryWithPolling();
  const counter = data?.modelQuality?.meanPerFile[0].probTotMean ?? 0;

  return (
    <Board
      header={<SectionTitle size="small" title="Probability overall" />}
      main={(
        <div className="flex flex-col h-full items-center justify-center gap-4">
          <div className="flex flex-row items-end ">

            {/* FIXME: inline style */}
            <div className="font-bold text-6xl" style={{ fontFamily: 'var(--coo-header-font)' }}>{numberFormatter().format(counter)}</div>
          </div>

        </div>
        )}
      modifier="h-full shadow"
      size="small"
      type="secondary"
    />
  );
}

export default BoardRow;
