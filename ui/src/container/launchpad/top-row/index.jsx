import { Board, NewHeader, SectionTitle } from '@radicalbit/radicalbit-design-system';
import { ExternalPathsEnum } from '@Src/constants';
import { memo } from 'react';
import Animation from '@Img/rocket-02.gif';
import CTAbackground from '@Img/RDBbackground.png';

function TopRow() {
  return (
    <div className="grid grid-cols-[auto,auto,1fr,1fr] px-4 gap-4 h-[175px] auto-rows-auto">
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
      style={{
        borderRadius: '.25rem',
      }}
      title="Radicalbit in Action: Open Source AI Monitoring for Regression Models"
      width="312px"
    />
  );
}

function TrialBoard() {
  const handleOnclick = () => {
    window.open(ExternalPathsEnum.BOOK_A_DEMO, '_blank');
  };

  return (
    <Board
      backgroundImage={CTAbackground}
      main={(
        <div className="flex flex-row items-center h-full pl-4 ">

          <div className="flex flex-col gap-2 justify-center mr-20">
            <SectionTitle title="Unlock the Full Potential" />

            <p className="leading-snug">Upgrade now and access advanced MLOps & LLMOps features, premium support and enhanced scalability</p>

            <SectionTitle
              modifier="montserrat-headers"
              size="large"
              style={{ color: 'var(--coo-highlight)' }}
              title="BOOK A DEMO"
              titleWeight="bold"
              wrapTitle
            />
          </div>

          <div className="absolute right-0 flex items-end h-full">
            <img alt="test" className="w-[8rem]" src={Animation} />
          </div>
        </div>
      )}
      modifier="light border-none p-0"
      onClick={handleOnclick}
      size="small"
      type="primary"
    />
  );
}

export default memo(TopRow);
