import InstructionsComponent from '@Container/tracing/project-detail/void-instructions';
import ApiKeysProject from './api-keys';

function Settings() {
  return (
    <div className="flex flex-col gap-4 items-center mb-10">
      <ApiKeysProject />

      <InstructionsComponent />
    </div>
  );
}

export default Settings;
