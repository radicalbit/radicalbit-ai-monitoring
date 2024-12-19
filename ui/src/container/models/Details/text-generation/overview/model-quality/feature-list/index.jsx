import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import {
  Board,
  NewHeader, Spinner, Tag, Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { Virtuoso } from 'react-virtuoso';
import { numberFormatter } from '@Src/constants';
import WordBarChart from '@Container/models/Details/text-generation/overview/model-quality/feature-list/chart';
import MarkdownToJsx, { RuleType } from 'markdown-to-jsx';
import useGetFilteredFeatures from './use-get-filtered-features';

function TextGenerationFeatureList() {
  const { tokens } = useGetFilteredFeatures();

  if (tokens.length === 0) {
    return (<NoFeaturesAvailable />);
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
  const { meanPerPhrase } = useGetFilteredFeatures();

  const perplexity = meanPerPhrase?.find((el) => el.id === token.id)?.perplexPerPhrase;
  const probability = meanPerPhrase?.find(({ id }) => id === token.id)?.probPerPhrase;

  const formattedPerplexity = perplexity ? Number.parseFloat(perplexity).toExponential(2) : '--';
  const formattedProbability = perplexity ? Number.parseFloat(probability).toExponential(2) : '--';
  return (
    <Board
      key={token.id}
      header={(
        <NewHeader
          details={{
            one: (
              <Tag type="secondary-light">
                Perplexity
                {' '}

                { formattedPerplexity}

              </Tag>),
            two: (
              <Tag>
                Confidence
                {' '}

                {formattedProbability}
              </Tag>),
          }}
        />
    )}
      main={(
        <div className="flex flex-col gap-4">
          <div className="flex flex-row gap-4">
            <div className="basis-11/12">
              <WordHintWithoutEffect token={token} />
            </div>

            <div className="basis-1/12">
              <WordHint token={token} />
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

function WordHint({ token }) {
  const { probs } = token;

  const regeExp = /\n/g;
  if (!token) {
    return false;
  }

  return (
    <div className="flex flex-row flex-wrap gap-1">
      {probs.map((p) => {
        const className = p.prob > 0.5 ? 'text-gen-color-green' : 'text-gen-color-red';

        if (regeExp.test(p.token)) {
          return (
            <Tooltip placement="top" title={numberFormatter().format(p.prob)}>
              <i className={className} style={{ '--text-gen-opacity': p.prob > 0.5 ? p.prob : 1 - p.prob }}>\n </i>
            </Tooltip>
          );
        }
        return (
          <Tooltip placement="top" title={numberFormatter().format(p.prob)}>
            <span className={className} style={{ '--text-gen-opacity': p.prob > 0.5 ? p.prob : 1 - p.prob }}>
              {p.token}
            </span>
          </Tooltip>
        );
      })}
    </div>
  );
}

function WordHintWithoutEffect({ token }) {
  const { probs } = token;

  const text = probs.reduce((acc, value) => acc + value.token, '');

  if (!token) {
    return false;
  }

  return (
    <div>
      <Markdown>
        {text}
      </Markdown>
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
              <pre key={state.key} style={{ backgroundColor: 'var(--coo-secondary-04)', padding: '.75rem', whiteSpace: 'pre-wrap' }}>
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
