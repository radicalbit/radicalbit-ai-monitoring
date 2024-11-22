import { Board, NewHeader, SectionTitle } from '@radicalbit/radicalbit-design-system';
import { ExternalPathsEnum } from '@Src/constants';
import { memo } from 'react';
import Logo from '@Img/rocket-02.gif';

function TopRow() {
  return (
    <div className="grid grid-cols-[1.2fr,1.2fr,1.2fr,1fr] px-4 gap-4 h-[175px]">
      <QuickStartBoard />

      <DocumentationHubBoard />

      <TrialBoard />

      <YoutubeVideoBoard />

    </div>
  );
}

function QuickStartBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.QUICKSTART, '_blank');
  };

  return (
    <Board
      footer={(
        <a>
          {'Get Started >>'}
        </a>
      )}
      header={(
        <NewHeader
          title={(
            <SectionTitle
              title="Quickstart guide 🚀"
              titleColor="primary"
              titleWeight="normal"
            />
            )}
        />
        )}
      main={(
        <div className="flex flex-col items-start gap-4 leading-snug">
          <div className="flex flex-col items-start">
            <strong>Get Up and Running in Minutes</strong>

            <p>A step-by-step guide to quickly setting up and using our AI monitoring platform</p>
          </div>
        </div>
      )}
      onClick={handleOnclick}
      size="small"
    />
  );
}

function DocumentationHubBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.DOCUMENTATION, '_blank');
  };

  return (
    <Board
      footer={(
        <a>
          {'Get Started >>'}
        </a>
      )}
      header={(
        <NewHeader
          title={(
            <SectionTitle
              title="Documentation Hub 📚​"
              titleColor="primary"
              titleWeight="normal"
            />
            )}
        />
        )}
      main={(
        <div className="flex flex-col items-start gap-4 leading-snug">
          <div className="flex flex-col items-start">
            <strong>Your Complete Resource</strong>

            <p>From setup to advanced configurations, find everything you need to navigate our platform</p>

          </div>

        </div>
      )}
      onClick={handleOnclick}
      size="small"
    />
  );
}

function YoutubeVideoBoard() {
  return (
    <iframe
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      allowFullScreen
      frameBorder="0"
      height="175px"
      referrerPolicy="strict-origin-when-cross-origin"
      src={`${ExternalPathsEnum.IFRAME_VIDEO}`}
      style={{ borderRadius: '.25rem', minWidth: '270px' }}
      title="Radicalbit in Action: Open Source AI Monitoring for Regression Models"
      width="100%"
    />
  );
}

function TrialBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.BOOK_A_DEMO, '_blank');
  };

  return (
    <Board
      main={(
        <div className="flex flex-row px-8">

          <div className="flex flex-col items-start gap-2 p-4 px-0">
            <SectionTitle title="Unlock the Full Potential" />

            <p className="leading-snug">Upgrade now and access advanced MLOps & LLMOps features, premium support and enhanced scalability</p>

            <SectionTitle
              size="large"
              style={{ color: 'var(--coo-highlight)' }}
              title="Book a demo"
              titleWeight="bold"
              wrapTitle
            />
          </div>

          <div>
            <img alt="test" className="w-[10rem] h-full" src={Logo} />
          </div>
        </div>
      )}
      modifier="h-full shadow light border-none p-0"
      onClick={handleOnclick}
      size="small"
      type="primary"
    />
  );
}

export default memo(TopRow);
