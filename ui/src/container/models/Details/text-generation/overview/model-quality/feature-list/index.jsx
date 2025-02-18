import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import WordBarChart from '@Container/models/Details/text-generation/overview/model-quality/feature-list/chart';
import {
  faChevronDown,
  faChevronUp,
  faFire,
  faM,
} from '@fortawesome/free-solid-svg-icons';
import {
  Board,
  FontAwesomeIcon,
  NewHeader,
  Spinner,
  StatusSelector,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { numberFormatter } from '@Src/constants';
import MarkdownToJsx, { RuleType } from 'markdown-to-jsx';
import { useState } from 'react';
import useGetFilteredFeatures from './use-get-filtered-features';

function TextGenerationFeatureList() {
  const { tokens } = useGetFilteredFeatures();

  if (tokens.length === 0) {
    return <NoFeaturesAvailable />;
  }

  return (
    <Spinner fullHeight fullWidth>
      {tokens.map((token) => <ColoredTokenBoard token={token} />)}
    </Spinner>
  );
}

function ColoredTokenBoard({ token }) {
  const [collapsed, setCollapsed] = useState(true);
  const [showHeatText, setShowHeatText] = useState(true);

  const handleOnClickCollapse = () => { setCollapsed(!collapsed); };
  const handleOnClickShowHeatText = () => { setShowHeatText(!showHeatText); };

  const collapsedIcon = collapsed ? faChevronDown : faChevronUp;
  const collapsedTooltipText = collapsed ? 'Click to expand' : 'Click to reduce';

  const showHeatTextIcon = showHeatText ? faM : faFire;
  const showHeatTextTooltipText = showHeatText ? 'Swicth to markdown format' : 'Switch to heatmap format';

  const { messageContent } = token;

  if (collapsed) {
    return (
      <Board
        key={token.id}
        header={(
          <NewHeader
            details={{
              one: (<Tooltip title={collapsedTooltipText}><FontAwesomeIcon icon={collapsedIcon} onClick={handleOnClickCollapse} /></Tooltip>),
            }}
            title={(<ColoredTokenBoardTitle token={token} />)}
          />
        )}
        main={(<ColoredTokenBoardBody token={token} withDot />)}
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
            one: (<Tooltip title={showHeatTextTooltipText}><FontAwesomeIcon icon={showHeatTextIcon} onClick={handleOnClickShowHeatText} /></Tooltip>),
            two: (<Tooltip title={collapsedTooltipText}><FontAwesomeIcon icon={collapsedIcon} onClick={handleOnClickCollapse} /></Tooltip>),
          }}
          title={(<ColoredTokenBoardTitle token={token} />)}
        />
      )}
      main={(
        <div className="flex flex-col gap-4">
          {!showHeatText && <Markdown>{messageContent}</Markdown>}

          {showHeatText && (<ColoredTokenBoardBody token={token} />)}
        </div>
      )}
      modifier="my-4 "
      size="small"
    />
  );
}

function ColoredTokenBoardBody({ token, withDot = false }) {
  const [barChartSelectedIndex, setBarChartSelectedIndex] = useState();

  const probs = withDot ? token?.probs?.toSpliced(90) : token?.probs;

  if (!probs) {
    return false;
  }

  if (withDot) {
    return (
      <div className="flex flex-row flex-wrap">

        {probs.map((tokenWithProb, idx) => (
          <TokenWithTooltip
            barChartSelectedIndex={barChartSelectedIndex}
            data={tokenWithProb}
            idx={idx}
            setBarChartSelectedIndex={setBarChartSelectedIndex}
          />
        ))}

        <span>...</span>
      </div>
    );
  }

  return (
    <>
      <div className="flex flex-row flex-wrap">

        {probs.map((tokenWithProb, idx) => (
          <TokenWithTooltip
            barChartSelectedIndex={barChartSelectedIndex}
            data={tokenWithProb}
            idx={idx}
            setBarChartSelectedIndex={setBarChartSelectedIndex}
          />
        ))}

      </div>

      <WordBarChart
        barChartSelectedIndex={barChartSelectedIndex}
        dataset={token}
      />
    </>
  );
}

function ColoredTokenBoardTitle({ token }) {
  const formattedPerplexity = token.perplexity
    ? numberFormatter().format(token.perplexity)
    : '--';

  const formattedProbability = token.probability
    ? numberFormatter().format(token.probability)
    : '--';

  const modelName = token.modelName ? token.modelName : '--';
  const rbitTimestamp = token.rbitTimestamp ? token.rbitTimestamp : '--';
  const totalToken = token.totalToken ? token.totalToken : '--';

  return (
    <div className="flex flex-row gap-4">

      <StatusSelector status={{ current: formattedProbability }} title="probability" />

      <StatusSelector status={{ current: formattedPerplexity }} title="Perplexity" />

      <StatusSelector status={{ current: totalToken }} title="N.Token" />

      <StatusSelector status={{ current: modelName }} title="Model" />

      <StatusSelector status={{ current: rbitTimestamp }} title="Created at" />

    </div>
  );
}

const regeExp = /\n/g;

function TokenWithTooltip({
  data, idx, barChartSelectedIndex, setBarChartSelectedIndex,
}) {
  const [showTooltip, setShowTooltip] = useState(false);

  const probability = data?.prob;
  const token = data?.token;

  const className = `whitespace-break-spaces text-prob ${probability <= 0.33 ? 'text-prob-danger' : probability > 0.33 && probability <= 0.66 ? 'text-prob-warning' : 'text-prob-success'}`;

  const textOpacityByProbability = {
    '--text-gen-opacity': probability > 0.5 ? probability : 1 - probability,
  };

  const borderSelectedToken = barChartSelectedIndex === idx ? 'border-1 border-solid' : '';

  const handleOnHover = () => {
    setShowTooltip((b) => !b);
  };

  const handleOnClick = () => {
    setBarChartSelectedIndex(idx);
  };

  if (regeExp.test(token)) {
    return (
      <i className={`${className}`} style={textOpacityByProbability}>
        \n
      </i>
    );
  }

  if (!showTooltip) {
    return (
      <span
        className={`${className} ${borderSelectedToken}`}
        onFocus={handleOnHover}
        onMouseOver={handleOnHover}
        style={textOpacityByProbability}
      >
        {token}
      </span>
    );
  }

  return (
    <Tooltip title={`probability: ${numberFormatter().format(probability)}`}>
      <span
        className={`${className} ${borderSelectedToken}`}
        onBlur={handleOnHover}
        onClick={handleOnClick}
        onMouseLeave={handleOnHover}
        style={textOpacityByProbability}
      >
        {token}
      </span>
    </Tooltip>
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
