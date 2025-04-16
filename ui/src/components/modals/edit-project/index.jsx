import useAutoFocus from '@Hooks/use-auto-focus';
import useModals from '@Hooks/use-modals';
import { tracingApiSlice } from '@State/tracing/api';
import { FormbitContextProvider, useFormbitContext } from '@radicalbit/formbit';
import {
  Button,
  FormField, Input, RbitModal, SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { useEffect, useRef } from 'react';
import { Skeleton } from 'antd';
import SomethingWentWrong from '@Components/ErrorPage/something-went-wrong';
import schema from './schema';
import useHandleOnSubmit from './use-handle-on-submit';

const { useGetProjectByUUIDQuery } = tracingApiSlice;

function EditProjectModal() {
  return (
    <FormbitContextProvider initialValues={{ name: null }} schema={schema}>
      <EditProjectModalInner />
    </FormbitContextProvider>
  );
}

function EditProjectModalInner() {
  const { hideModal } = useModals();
  const { error } = useFormbitContext();

  useInitializeForm();

  return (
    <RbitModal
      actions={(<Actions />)}
      header={<SectionTitle align="center" title="Edit Project" titleColor="primary" />}
      headerType="light"
      onCancel={hideModal}
      open
    >
      <>
        <ProjectName />

        {error('silent.backend') && <FormField message={error('silent.backend')} />}
      </>
    </RbitModal>
  );
}

function ProjectName() {
  const ref = useRef(null);

  const { modalPayload: { data: { uuid } } } = useModals();
  const { form, error, write } = useFormbitContext();
  const { isLoading, isError } = useGetProjectByUUIDQuery({ uuid });

  const { handleOnSubmit, args: { isLoading: isEditing } } = useHandleOnSubmit();

  const handleOnChange = ({ target: { value } }) => {
    write('name', value);
  };

  useAutoFocus(ref);

  if (isLoading) {
    return <Skeleton.Input active block />;
  }

  if (isError) {
    return <SomethingWentWrong />;
  }

  return (
    <FormField label="Name" message={error('name')} modifier="w-full" required>
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnSubmit}
        readOnly={isEditing}
        ref={ref}
        value={form.name}
      />
    </FormField>
  );
}

function Actions() {
  const { hideModal } = useModals();
  const { handleOnSubmit, args, isSubmitDisabled } = useHandleOnSubmit();

  return (
    <>
      <Button onClick={hideModal}>Cancel</Button>

      <Button
        disabled={isSubmitDisabled}
        loading={args.isLoading}
        onClick={handleOnSubmit}
        type="primary"
      >
        Save Project
      </Button>
    </>
  );
}

const useInitializeForm = () => {
  const { modalPayload: { data: { uuid } } } = useModals();

  const { data, isSuccess } = useGetProjectByUUIDQuery({ uuid });
  const name = data?.name;

  const { initialize } = useFormbitContext();

  useEffect(() => {
    if (isSuccess) {
      initialize({ name });
    }
  }, [initialize, isSuccess, name]);
};

export default EditProjectModal;
