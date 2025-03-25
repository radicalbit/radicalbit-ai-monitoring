import MarkdownToJsx, { RuleType } from 'markdown-to-jsx';
import { useParams } from 'react-router';
import { Board, SectionTitle } from '@radicalbit/radicalbit-design-system';
import tracingInstructions from './tracing-instructions.md?raw';

function InstructionsComponent() {
  return (
    <Board
      header={(
        <SectionTitle
          size="large"
          title="How to connect"
          titleColor="primary"
        />
    )}
      main={(
        <MarkdownRenderComponent />
      )}
      modifier="max-w-[800px] w-full"
    />
  );
}

function MarkdownRenderComponent() {
  const { uuid } = useParams();

  const traceWithUUID = tracingInstructions.replace(
    "f'{project_uuid}'",
    `"${uuid}"`,
  );

  return (
    <MarkdownToJsx
      options={{
        renderRule(next, node, _, state) {
          switch (node.type) {
            case RuleType.codeBlock:
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
            case RuleType.link:
              return (
                <a
                  className="underline"
                  href={node.target}
                  style={{ color: 'var(--coo-primary-01)' }}
                >
                  {node.children[0].text}
                </a>
              );
            default:
              return next();
          }
        },
      }}
    >
      {traceWithUUID}
    </MarkdownToJsx>
  );
}

export default InstructionsComponent;
