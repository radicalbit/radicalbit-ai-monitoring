import SiderBk from '@Img/sider-bk.png';
import Logo from '@Src/components/Logo';
import ModalsProvider from '@Src/components/modals/modals-provider';
import { useContextConfigurationFromUrlEffect } from '@Src/store/state/context-configuration/hooks';
import { useNotification } from '@Src/store/state/notification/hooks';
import { actions as layoutActions, selectors as layoutSelectors } from '@State/layout';
import '@Styles/index.less';
import '@Styles/tailwind.less';
import { Layout } from '@radicalbit/radicalbit-design-system';
import { useDispatch, useSelector } from 'react-redux';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import CookieConsent from 'react-cookie-consent';
import { CHART_COLOR } from '@Helpers/common-chart-options';
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

  const isAllDark = useSelector(layoutSelectors.selectIsAllDark);

  const hasHeaderContentDark = useSelector(layoutSelectors.selectHasHeaderContentDark);

  const isMainContentDark = useSelector(layoutSelectors.selectHasMainContentDark);
  const hasMainContentDark = isAllDark || isMainContentDark;

  const hasHeader = useSelector(layoutSelectors.selectHasHeader);
  const isSecondaryColumn = useSelector(layoutSelectors.selectHasSecondaryColumn);
  const isLeftColumnCollapsed = useSelector(layoutSelectors.selectHasLeftColumnCollapsed);
  const hasSecondaryContentDark = useSelector(layoutSelectors.selectHasSecondaryContentDark);
  const hasHeaderSecondaryContentDark = useSelector(layoutSelectors.selectHasHeaderSecondaryContentDark);
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
          hasHeaderLeftContentDark: true,
          hasLeftColumnCollapsed,
          hasLeftContentDark: true,
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
        buttonStyle={{ color: CHART_COLOR.WHITE, background: CHART_COLOR.CURRENT_DARK, borderRadius: 50 }}
        buttonText="Accept"
        cookieName="rbit-tracking"
        declineButtonStyle={{ color: CHART_COLOR.WHITE, background: CHART_COLOR.CURRENT_DARK, borderRadius: 50 }}
        declineButtonText="Decline"
        enableDeclineButton
        expires={150}
        location="bottom"
        onAccept={handleOnAccept}
      >
        This website uses cookies to enhance the user experience.
        {' '}

        <span style={{ fontSize: '10px' }}>This bit of text is smaller :O</span>
      </CookieConsent>
    </>
  );
}
