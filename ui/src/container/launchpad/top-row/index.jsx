import { Board, NewHeader, SectionTitle } from '@radicalbit/radicalbit-design-system';
import { ExternalPathsEnum } from '@Src/constants';
import { memo } from 'react';
import { Link } from 'react-router-dom';

function TopRow() {
  return (
    <div className="grid grid-cols-[1.5fr,1.5fr,1fr,1.5fr] gap-4 max-h-[185px]">

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
        <div className="flex flex-col items-start gap-4 leading-snug">
          <div className="flex flex-col items-start">
            <p className="font-bold text-">Get Up and Running in Minutes</p>

            <p>A step-by-step guide to quickly setting up and using our AI monitoring platform</p>

          </div>

          <Link onClick={handleOnclick}>
            <div className="text-xl">
              {'Get Started >>'}
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
        <div className="flex flex-col items-start gap-4 leading-snug">
          <div className="flex flex-col items-start">
            <p className="font-bold text-">Your Complete Resource</p>

            <p>From setup to advanced configurations, find everything you need to navigate our platform</p>

          </div>

          <Link onClick={handleOnclick}>
            <div className="text-xl">
              {'Get Started >>'}
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
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowFullScreen
      frameBorder="0"
      height="182px"
      referrerPolicy="strict-origin-when-cross-origin"
      src={`${ExternalPathsEnum.IFRAME_VIDEO}`}
      style={{ borderRadius: '1rem', minWidth: '325px' }}
      title="Radicalbit in Action: Open Source AI Monitoring for Regression Models"
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

          <p className="leading-snug">Upgrade now and access advanced MLOps & LLMOps features, premium support and enhanced scalability</p>

          <SectionTitle
            size="large"
            style={{ color: 'var(--coo-highlight)' }}
            title="Start your free trial today!"
            titleWeight="bold"
            wrapTitle
          />

        </div>
      )}
      modifier="h-full shadow light border-none"
      onClick={handleOnclick}
      type="primary"
    />
  );
}

export default memo(TopRow);
