import { useFormbitContext } from '@radicalbit/formbit';
import {
  Board,
  Button,
  FormField,
  Input,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';

function EditProject() {
  const { form, isFormInvalid, isDirty } = useFormbitContext();

  const handleOnClick = () => {
    console.debug(form.editedName);
  };

  const isButtonDisabled = isFormInvalid() || !isDirty;

  return (
    <Board
      header={(
        <SectionTitle
          size="large"
          subtitle={`Your Project is currently named ${form.name}`}
          title="Edit project name"
          titleColor="primary"
        />
      )}
      main={(
        <div className="flex flex-row justify-between items-end">
          <EditProjectInput />

          <Button disabled={isButtonDisabled} onClick={handleOnClick}>Save Project</Button>
        </div>
      )}
      modifier="max-w-[800px] w-full"
    />
  );
}

function EditProjectInput() {
  const { form, error, write } = useFormbitContext();

  const handleOnChange = ({ target: { value } }) => {
    write('editedName', value);
  };

  return (
    <FormField className="w-80" message={error('editedName')} required>
      <Input
        onChange={handleOnChange}
        placeholder={form.name}
        value={form.editedName}
      />
    </FormField>
  );
}

export default EditProject;
