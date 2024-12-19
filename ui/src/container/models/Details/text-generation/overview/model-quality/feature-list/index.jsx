import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import {
  Board, Button, FontAwesomeIcon, NewHeader, Spinner, Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { Virtuoso } from 'react-virtuoso';
import { fa1 } from '@fortawesome/free-solid-svg-icons';
import useGetFilteredFeatures from './use-get-filtered-features';

function TextGenerationFeatureList() {
  const tokens = useGetFilteredFeatures();

  if (tokens.length === 0) {
    return (<NoFeaturesAvailable />);
  }

  return (
    <Spinner fullHeight fullWidth>
      <Virtuoso
        data={tokens}
        itemContent={(index, token) => <TokenBoard token={token} />}
        totalCount={tokens.length}
      />
    </Spinner>
  );
}

function TokenBoard({ token }) {
  return (
    <Board
      key={token.id}
      header={(
        <NewHeader
          details={{
            one: (
              <Button
                shape="circle"
                size="small"
                title="1"
                type="primary"
              >
                <FontAwesomeIcon icon={fa1} />
              </Button>
            ),
          }}
        />
    )}
      main={(
        <div className="flex flex-row gap-4">
          <WordHintWithoutEffect token={token} />

          <WordHint token={token} />
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
        if (regeExp.test(p.token)) {
          return (
            <Tooltip placement="top" title={p.prob}>
              <i className="text-gen-color" style={{ '--text-gen-opacity': p.prob }}>\n </i>
            </Tooltip>
          );
        }
        return (
          <Tooltip placement="top" title={p.prob}>
            <span className="cursor-pointer text-gen-color" style={{ '--text-gen-opacity': p.prob }}>
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

  const regeExp = /\n/g;
  if (!token) {
    return false;
  }

  return (
    <div className="flex flex-row flex-wrap gap-1">
      {probs.map((p) => {
        if (regeExp.test(p.token)) {
          return (<i>\n </i>);
        }
        return (<span>{p.token}</span>);
      })}
    </div>
  );
}

export default TextGenerationFeatureList;
