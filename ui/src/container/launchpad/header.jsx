import { NewHeader, SectionTitle } from '@radicalbit/radicalbit-design-system';

export default function MainListModelsHeader() {
  const title = 'AI Monitoring Launchpad';
  const subtitle = 'a comprehensive dashboard to track model performance, access setup resources, review alerts and ensure data completeness.';

  return (
    <NewHeader
      title={(
        <>
          <h1>{title}</h1>

          <SectionTitle subtitle={subtitle} />
        </>
      )}
    />
  );
}
