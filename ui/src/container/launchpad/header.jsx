import {
  MAIN_LAYOUT_DARK_MODE_CONFIGURATION,
  MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION,
} from '@Container/layout/layout-provider/layout-provider-configuration';
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons';
import {
  Button,
  FontAwesomeIcon, NewHeader, SectionTitle, Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { useState } from 'react';
import { useDispatch } from 'react-redux';

export default function MainListModelsHeader() {
  const title = 'AI Monitoring Launchpad';
  const subtitle = 'a comprehensive dashboard to track model performance, access setup resources, review alerts and ensure data completeness.';

  return (
    <NewHeader
      actions={{
        one: <DarkMode />,
        two: <div />,
      }}
      title={(
        <>
          <h1>{title}</h1>

          <SectionTitle subtitle={subtitle} />
        </>
      )}
    />
  );
}

function DarkMode() {
  const dispatch = useDispatch();
  const [isDarkMode, setIsDarkMode] = useState(!!window.localStorage.getItem('enable-dark-mode'));

  const handleOnEnableDarkMode = () => {
    window.localStorage.setItem('enable-dark-mode', true);
    setIsDarkMode(true);

    MAIN_LAYOUT_DARK_MODE_CONFIGURATION.forEach((action) => dispatch(action()));
  };

  const handleOnEnableLightMode = () => {
    window.localStorage.removeItem('enable-dark-mode');
    setIsDarkMode(false);

    MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION.forEach((action) => dispatch(action()));
  };

  if (isDarkMode) {
    return (
      <Tooltip title="Switch to light mode">
        <Button onClick={handleOnEnableLightMode} type="text"><FontAwesomeIcon icon={faMoon} /></Button>
      </Tooltip>
    );
  }

  return (
    <Tooltip title="Switch to dark mode">
      <Button onClick={handleOnEnableDarkMode} type="text"><FontAwesomeIcon icon={faSun} /></Button>
    </Tooltip>
  );
}
