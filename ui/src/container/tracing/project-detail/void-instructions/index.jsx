import MarkdownToJsx, { RuleType } from 'markdown-to-jsx';
import tracingInstructions from './tracing-instructions.md?raw';

function InstructionsComponent() {
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
              return <a className="underline" href={node.target} style={{ color: 'var(--coo-primary-01)' }}>{node.children[0].text}</a>;
            default:
              return next();
          }
        },
      }}
    >
      {tracingInstructions}
    </MarkdownToJsx>
  );
}

export default InstructionsComponent;
