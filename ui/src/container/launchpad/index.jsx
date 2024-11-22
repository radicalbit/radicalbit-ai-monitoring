import { useInitDarkMode } from '@Components/dark-mode/hooks';
import { MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import ModelStatsList from './model-stats-list';
import TopRow from './top-row';
import AlertList from './alerts-list';
import WorkInProgress from './work-in-progress';

export default function Launchpad() {
  useInitDarkMode(MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION);

  return (
    <div className="flex flex-col gap-4 h-full">
      <TopRow />

      <ModelStatsList />

      <WorkInProgress />

      <AlertList />

    </div>
  );
}
