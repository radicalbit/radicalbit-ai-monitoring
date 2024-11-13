import SiderBk from '@Img/sider-bk.png';
import Logo from '@Src/components/Logo';
import ModalsProvider from '@Src/components/modals/modals-provider';
import { useContextConfigurationFromUrlEffect } from '@State/context-configuration/hooks';
import { useNotification } from '@State/notification/hooks';
import { actions as layoutActions, selectors as layoutSelectors } from '@State/layout';
import '@Styles/index.less';
import '@Styles/tailwind.less';
import { Layout } from '@radicalbit/radicalbit-design-system';
import CookieConsent from 'react-cookie-consent';
import { useDispatch, useSelector } from 'react-redux';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { createRoutes } from '../layout';
import { useLayoutProvider } from '../layout/layout-provider';
import BottomMenu from './bottom-menu';
import MainHeaderContentSwitch from './content-switch/header';
import SecondaryContentSwitch from './content-switch/secondary-column/content';
import SecondaryHeaderContentSwitch from './content-switch/secondary-column/header';

export default function App() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  useLayoutProvider();

  useNotification();
  useContextConfigurationFromUrlEffect();

  const hasHeaderContentDark = useSelector(layoutSelectors.selectHasHeaderContentDark);
  const hasHeaderLeftContentDark = useSelector(layoutSelectors.selectHasHeaderLeftContentDark);
  const hasHeaderSecondaryContentDark = useSelector(layoutSelectors.selectHasHeaderSecondaryContentDark);
  const hasLeftContentDark = useSelector(layoutSelectors.selectHasLeftContentDark);
  const hasMainContentDark = useSelector(layoutSelectors.selectHasMainContentDark);
  const hasSecondaryContentDark = useSelector(layoutSelectors.selectHasSecondaryContentDark);

  const hasHeader = useSelector(layoutSelectors.selectHasHeader);
  const isSecondaryColumn = useSelector(layoutSelectors.selectHasSecondaryColumn);
  const isLeftColumnCollapsed = useSelector(layoutSelectors.selectHasLeftColumnCollapsed);
  const hasSecondaryColumnCollapsed = useSelector(layoutSelectors.selectHasSecondaryColumnCollapsed);

  const hasSecondaryColumn = isSecondaryColumn;
  const hasLeftColumnCollapsed = isLeftColumnCollapsed;

  const showBottomDrawerOnHover = useSelector(layoutSelectors.selectShowBottomDrawerOnHover);

  const handleToggleCollapseLeftColumn = () => {
    dispatch(layoutActions.toggleCollapseLeftColumn());
  };

  const handleToggleCollapseSecondaryColumn = () => {
    dispatch(layoutActions.toggleCollapseSecondaryColumn());
  };

  const goToHomePage = () => {
    navigate('/');
  };

  const handleOnAccept = () => {
    window.location.reload();
  };

  return (
    <>
      <Layout
        hasHeader={hasHeader}
        hasLeftColumn
        hasMainColumn
        hasOverallTop={false}
        hasRightColumn={false}
        hasSecondaryColumn={hasSecondaryColumn}
        left={{
          hasHeaderLeftContentDark,
          hasLeftColumnCollapsed,
          hasLeftContentDark,
          leftColumnHeaderAltContent: <Logo onClick={goToHomePage} title="Radicalbit" />,
          backgroundImage: SiderBk,
          mainMenu: createRoutes({ currentPath: pathname }),
          onLeftColumnCollapse: handleToggleCollapseLeftColumn,
          bottomMenu: <BottomMenu />,
        }}
        main={{
          hasMainContentDark,
          hasHeaderContentDark,
          headerContent: <MainHeaderContentSwitch />,
          mainContent: <Outlet />,
          showBottomDrawerOnHover,
        }}
        secondary={{
          headerContent: <SecondaryHeaderContentSwitch />,
          mainContent: <SecondaryContentSwitch />,
          onSecondaryColumnCollapse: handleToggleCollapseSecondaryColumn,
          hasHeaderSecondaryContentDark,
          hasSecondaryColumnCollapsed,
          hasSecondaryContentDark,
          hasSecondaryColumn,
        }}
      />

      <ModalsProvider />

      <CookieConsent
        buttonClasses="ant-btn ant-btn-primary m-button px-8"
        buttonText="Allow anonymous"
        buttonWrapperClasses="flex gap-8 mr-5"
        cookieName="rbit-tracking"
        declineButtonClasses="ant-btn ant-btn-primary-light m-button px-16"
        declineButtonText="Do not allow"
        disableButtonStyles
        enableDeclineButton
        expires={365}
        location="bottom"
        onAccept={handleOnAccept}
        style={{ alignItems: 'center' }}
      >
        <h3>We Value Your Privacy</h3>

        <p>
          We collect anonymous usage data to improve our software. This information helps us understand how the software is used and identify areas for improvement.
          <br />
          No personally identifiable information is collected.
        </p>

      </CookieConsent>
    </>
  );
}
