import DarkMode from '@Components/dark-mode';
import { MAIN_LAYOUT_DARK_MODE_CONFIGURATION, MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION } from '@Container/layout/layout-provider/layout-provider-configuration';
import { NewHeader, SectionTitle } from '@radicalbit/radicalbit-design-system';

export default function MainListModelsHeader() {
  const title = 'AI Monitoring Launchpad';
  const subtitle = 'a comprehensive dashboard to track model performance, access setup resources, review alerts and ensure data completeness.';

  return (
    <NewHeader
      actions={{
        one: <DarkMode
          darkActions={MAIN_LAYOUT_DARK_MODE_CONFIGURATION}
          lightActions={MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION}
        />,
        two: <div style={{ width: '1rem', height: '1rem' }} />,
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
