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

function AddNewApiKeyModal() {
  return (
    <FormbitContextProvider initialValues={{ name: null }} schema={schema}>
      <AddNewApiKeyModalInner />
    </FormbitContextProvider>
  );
}

function AddNewApiKeyModalInner() {
  const { hideModal } = useModals();

  const { error } = useFormbitContext();

  return (
    <RbitModal
      actions={(<Actions />)}
      header={<SectionTitle align="center" title="New Api key" titleColor="primary" />}
      headerType="light"
      onCancel={hideModal}
      open
    >
      <>
        <ApiKeyName />

        {error('silent.backend') && <FormField message={error('silent.backend')} />}
      </>
    </RbitModal>
  );
}

function ApiKeyName() {
  const ref = useRef(null);

  const { form, error, write } = useFormbitContext();
  const { handleOnSubmit, args: { isLoading } } = useHandleOnSubmit();

  const handleOnChange = ({ target: { value } }) => {
    write('name', value);
  };

  useAutoFocus(ref);

  return (
    <FormField label="Name" message={error('name')} modifier="w-full" required>
      <Input
        onChange={handleOnChange}
        onPressEnter={handleOnSubmit}
        readOnly={isLoading}
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
        Save
      </Button>
    </>
  );
}

export default AddNewApiKeyModal;
