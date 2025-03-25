import InstructionsComponent from '@Container/tracing/project-detail/void-instructions';
import { FormbitContextProvider, useFormbitContext } from '@radicalbit/formbit';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useEffect } from 'react';
import { useParams } from 'react-router';
import DeleteProject from './delete-project';
import EditProject from './edit-project';
import schema from './schema';

const { useGetProjectByUUIDQuery } = tracingApiSlice;

function Settings() {
  return (
    <FormbitContextProvider initialValues={{ name: null }} schema={schema}>
      <SettingsInner />
    </FormbitContextProvider>
  );
}

function SettingsInner() {
  useInitializeForm();

  return (
    <div className="flex flex-col gap-4 items-center ">
      <EditProject />

      <DeleteProject />

      <InstructionsComponent />
    </div>
  );
}

const useInitializeForm = () => {
  const { uuid } = useParams();
  const { data, isSuccess } = useGetProjectByUUIDQuery({ uuid });
  const name = data?.name;

  const { initialize } = useFormbitContext();

  useEffect(() => {
    if (isSuccess) {
      initialize({ name });
    }
  }, [initialize, isSuccess, name]);
};

export default Settings;
