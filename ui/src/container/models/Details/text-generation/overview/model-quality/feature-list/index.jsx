import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import WordBarChart from '@Container/models/Details/text-generation/overview/model-quality/feature-list/chart';
import {
  faExpand,
  faFire,
  faMinimize,
  faTextHeight,
} from '@fortawesome/free-solid-svg-icons';
import {
  Board,
  FontAwesomeIcon,
  NewHeader,
  Spinner,
  Tag,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import MarkdownToJsx, { RuleType } from 'markdown-to-jsx';
import { useState } from 'react';
import { Virtuoso } from 'react-virtuoso';
import useGetFilteredFeatures from './use-get-filtered-features';

function TextGenerationFeatureList() {
  const { tokens } = useGetFilteredFeatures();

  if (tokens.length === 0) {
    return <NoFeaturesAvailable />;
  }

  return (
    <Spinner fullHeight fullWidth>
      <Virtuoso
        data={tokens}
        itemContent={(_, token) => <TokenBoard token={token} />}
        totalCount={tokens.length}
      />
    </Spinner>
  );
}

function TokenBoard({ token }) {
  const [collapsed, setCollapsed] = useState(true);
  const [showHeatText, setShowHeatText] = useState(false);

  const { meanPerPhrase } = useGetFilteredFeatures();

  const messageContent = token.message_content;

  const perplexity = meanPerPhrase?.find(
    (el) => el.id === token.id,
  )?.perplexPerPhrase;

  const probability = meanPerPhrase?.find(
    ({ id }) => id === token.id,
  )?.probPerPhrase;

  const formattedPerplexity = perplexity ? numberFormatter().format(perplexity) : '--';
  const formattedProbability = perplexity ? numberFormatter().format(probability) : '--';

  const handleOnClick = () => setCollapsed(!collapsed);
  const handleOnToggle = () => setShowHeatText(!showHeatText);

  if (collapsed) {
    return (
      <Board
        key={token.id}
        header={(
          <NewHeader
            details={{
              one: (
                <FontAwesomeIcon
                  icon={collapsed ? faExpand : faMinimize}
                  onClick={handleOnClick}
                />
              ),
            }}
            title={(
              <div className="flex flex-row gap-4">
                <Tag type="full">
                  Perplexity
                  {' '}

                  {formattedPerplexity}
                </Tag>

                <Tag type="full">
                  Probability
                  {' '}

                  {formattedProbability}
                </Tag>
              </div>
            )}
          />
        )}
        main={(
          <div className="flex flex-col gap-4">
            <div className="flex flex-row gap-4">
              <div className="flex flex-col basis-11/12 gap-4">
                {messageContent.substr(0, 600)}
                ...
              </div>

              <div className="basis-1/12">
                <WordHint probs={token.probs.toSpliced(5)} />
              </div>
            </div>

            {/*   <WordBarChart dataset={token} /> */}
          </div>
        )}
        modifier="my-4 "
        size="small"
      />
    );
  }

  return (
    <Board
      key={token.id}
      header={(
        <NewHeader
          details={{
            one: (
              <FontAwesomeIcon
                icon={showHeatText ? faTextHeight : faFire}
                onClick={handleOnToggle}
              />
            ),
            two: (
              <FontAwesomeIcon
                icon={collapsed ? faExpand : faMinimize}
                onClick={handleOnClick}
              />
            ),
          }}
          title={(
            <div className="flex flex-row gap-4">
              <Tag type="full">
                Perplexity
                {' '}

                {formattedPerplexity}
              </Tag>

              <Tag type="full">
                Probability
                {' '}

                {formattedProbability}
              </Tag>
            </div>
          )}
        />
      )}
      main={(
        <div className="flex flex-col gap-4">
          <div className="flex flex-row gap-4 overflow-auto max-h-[40rem]">
            {!showHeatText && <Markdown>{messageContent}</Markdown>}

            {showHeatText && <WordHint probs={token.probs} />}
          </div>

          <WordBarChart dataset={token} />
        </div>
      )}
      modifier="my-4 "
      size="small"
    />
  );
}

function WordHint({ probs }) {
  const regeExp = /\n/g;
  if (!probs) {
    return false;
  }

  return (
    <div className="flex flex-row flex-wrap gap-1">
      {probs.map((p) => {
        const className = p.prob > 0.5 ? 'text-gen-color-green' : 'text-gen-color-red';

        if (regeExp.test(p.token)) {
          return (
            <Tooltip placement="top" title={numberFormatter().format(p.prob)}>
              <i
                className={className}
                style={{
                  '--text-gen-opacity': p.prob > 0.5 ? p.prob : 1 - p.prob,
                }}
              >
                \n
                {' '}
              </i>
            </Tooltip>
          );
        }
        return (
          <Tooltip placement="top" title={numberFormatter().format(p.prob)}>
            <span
              className={className}
              style={{
                '--text-gen-opacity': p.prob > 0.5 ? p.prob : 1 - p.prob,
              }}
            >
              {p.token}
            </span>
          </Tooltip>
        );
      })}
    </div>
  );
}

function Markdown({ children }) {
  return (
    <MarkdownToJsx
      options={{
        renderRule(next, node, _, state) {
          if (node.type === RuleType.codeBlock) {
            return (
              <pre
                key={state.key}
                style={{
                  backgroundColor: 'var(--coo-secondary-04)',
                  padding: '.75rem',
                  whiteSpace: 'pre-wrap',
                }}
              >
                {String.raw`${node.text}`}
              </pre>
            );
          }

          return next();
        },
      }}
    >
      {children}
    </MarkdownToJsx>
  );
}

export default TextGenerationFeatureList;
