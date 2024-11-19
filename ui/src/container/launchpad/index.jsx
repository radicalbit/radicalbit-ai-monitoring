import { useInitDarkMode } from '@Components/dark-mode/hooks';
import { MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import ModelStatsList from './central-row';
import RightColumn from './right-column';
import TopRow from './top-row';

export default function Launchpad() {
  useInitDarkMode(MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION);

  return (
    <div className="flex flex-col p-4 gap-4 h-full">
      <TopRow />

      <div className="grid grid-cols-[1.2fr,1.2fr,1fr,1.2fr] gap-4 h-full">
        <div className="col-span-3">
          <ModelStatsList />
        </div>

        <RightColumn />
      </div>
    </div>
  );
}
