import { Board, NewHeader, SectionTitle } from '@radicalbit/radicalbit-design-system';
import { ExternalPathsEnum } from '@Src/constants';
import { memo } from 'react';
import { Link } from 'react-router-dom';

function TopRow() {
  return (
    <div className="grid grid-cols-[1.5fr,1.5fr,1fr,1fr] gap-4">

      <QuickStartBoard />

      <DocumentationHubBoard />

      <YoutubeVideoBoard />

      <TrialBoard />
    </div>
  );
}

function QuickStartBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.QUICKSTART, '_blank');
  };

  return (
    <Board
      header={(
        <NewHeader
          details={{ one: (<span aria-label="tada" role="img">🎉</span>) }}
          title={(
            <SectionTitle
              title="Quickstart guide"
              titleColor="primary"
              titleWeight="normal"
            />
            )}
        />
        )}
      main={(
        <div className="flex flex-col items-start gap-4">
          <div className="flex flex-col items-start">
            <SectionTitle
              title="Get Up and Running in Minutes"
              titleWeight="normal"
              wrapTitle
            />

            <div>A step-by-step guide to quickly setting up and using our AI monitoring platform</div>

          </div>

          <Link onClick={handleOnclick}>
            <div className="text-xl">
              Get Started
            </div>
          </Link>

        </div>
      )}
      onClick={handleOnclick}
    />
  );
}

function DocumentationHubBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.DOCUMENTATION, '_blank');
  };

  return (
    <Board
      header={(
        <NewHeader
          details={{ one: (<span aria-label="man" role="img">👨</span>) }}
          title={(
            <SectionTitle
              title="Documentation Hub"
              titleColor="primary"
              titleWeight="normal"
            />
            )}
        />
        )}
      main={(
        <div className="flex flex-col items-start gap-4">
          <div className="flex flex-col items-start">
            <SectionTitle
              title="Your Complete Resource"
              titleWeight="normal"
            />

            <div>From setup to advanced configurations, find everything you need to navigate our platform</div>

          </div>

          <Link onClick={handleOnclick}>
            <div className="text-xl">
              Get Started
            </div>
          </Link>
        </div>
      )}
      onClick={handleOnclick}
    />
  );
}

function YoutubeVideoBoard() {
  return (

    <iframe
      frameBorder="0"
      height="100%"
      referrerPolicy="strict-origin-when-cross-origin"
      src={`${ExternalPathsEnum.IFRAME_VIDEO}`}
      style={{ borderRadius: '20px' }}
      title="Radicalbit in Action: Introducing Open Source AI Monitoring"
      width="100%"
    />
  );
}

function TrialBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.FREE_TRIAL, '_blank');
  };

  return (
    <Board
      main={(
        <div className="flex flex-col items-start gap-2">
          <SectionTitle title="Unlock the Full Potential" />

          <div>Upgrade now and access advanced MLOps & LLMOps features, premium support and enhanced scalability</div>

          <SectionTitle
            modifier="whitespace-normal"
            size="large"
            style={{ color: 'var(--coo-highlight)' }}
            title="Start your free trial today!"
            wrapTitle
          />

        </div>
      )}
      modifier="h-full shadow"
      onClick={handleOnclick}
      type="primary"
    />
  );
}

export default memo(TopRow);
