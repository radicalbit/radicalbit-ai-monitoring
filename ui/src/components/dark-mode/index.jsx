import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, Tooltip } from '@radicalbit/radicalbit-design-system';
import { useIsDarkMode, useSetDarkMode } from './hooks';

function DarkMode({ darkActions = [], lightActions = [] }) {
  const isDarkMode = useIsDarkMode();
  const { enableDarkMode, enableLightMode } = useSetDarkMode(darkActions, lightActions);

  if (isDarkMode) {
    return (
      <Tooltip title="Switch to light mode">
        <FontAwesomeIcon icon={faMoon} onClick={enableLightMode} />
      </Tooltip>
    );
  }

  return (
    <Tooltip title="Switch to dark mode">
      <FontAwesomeIcon icon={faSun} onClick={enableDarkMode} />
    </Tooltip>
  );
}

export default DarkMode;
