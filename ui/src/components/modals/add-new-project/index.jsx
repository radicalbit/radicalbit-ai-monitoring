import useAutoFocus from '@Hooks/use-auto-focus';
import useModals from '@Hooks/use-modals';
import { FormbitContextProvider, useFormbitContext } from '@radicalbit/formbit';
import {
  Button,
  FormField, Input, RbitModal, SectionTitle,
} from '@radicalbit/radicalbit-design-system';

import { useRef } from 'react';
import schema from './schema';
import useHandleOnSubmit from './use-handle-on-submit';

function AddNewProjectModal() {
  return (
    <FormbitContextProvider initialValues={{ name: null }} schema={schema}>
      <AddNewProjectModalInner />
    </FormbitContextProvider>
  );
}

function AddNewProjectModalInner() {
  const { hideModal } = useModals();

  return (
    <RbitModal
      actions={(<Actions />)}
      header={<SectionTitle align="center" title="New Project" titleColor="primary" />}
      headerType="light"
      onCancel={hideModal}
      open
    >
      <ProjectName />
    </RbitModal>
  );
}

function ProjectName() {
  const ref = useRef(null);
  const { form, error, write } = useFormbitContext();

  const handleOnChange = ({ target: { value } }) => {
    write('name', value);
  };

  useAutoFocus(ref);

  return (
    <FormField label="Name" message={error('name')} modifier="w-full" required>
      <Input
        onChange={handleOnChange}
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

export default AddNewProjectModal;
