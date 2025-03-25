import {
  Board, Button,
  Popconfirm,
  SectionTitle,
} from '@radicalbit/radicalbit-design-system';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useNavigate, useParams } from 'react-router';

const { useDeleteProjectMutation } = tracingApiSlice;

function DeleteProject() {
  return (
    <Board
      header={(
        <div className="flex flex-row justify-between items-end">
          <SectionTitle
            size="large"
            subtitle="Warning: this operation is irreversible"
            title="Delete project"
            titleColor="primary"
          />

          <DeleteButton />
        </div>
    )}
      modifier="max-w-[800px] w-full"
    />
  );
}

function DeleteButton() {
  const { uuid } = useParams();
  const navigate = useNavigate();

  const [triggerDeleteModel] = useDeleteProjectMutation();
  const handleOnClick = async () => {
    const response = await triggerDeleteModel({ uuid });

    if (response.error) {
      console.error(response.error);
      return;
    }

    navigate('/projects');
  };

  return (
    <Popconfirm
      label={<Button type="error-light">Delete Project</Button>}
      okText="Delete"
      okType="error-light"
      onCancel={null}
      onConfirm={handleOnClick}
      title=" Are you sure you want to delete this project? "
    />
  );
}

export default DeleteProject;
