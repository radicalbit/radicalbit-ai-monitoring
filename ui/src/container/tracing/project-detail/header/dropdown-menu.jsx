import { faEllipsisH } from '@fortawesome/free-solid-svg-icons';
import useModals from '@Hooks/use-modals';
import { Dropdown, FontAwesomeIcon, Popconfirm } from '@radicalbit/radicalbit-design-system';
import { ModalsEnum } from '@Src/constants';
import { tracingApiSlice } from '@State/tracing/api';
import { useNavigate, useParams } from 'react-router-dom';

const { useDeleteProjectMutation } = tracingApiSlice;

function DropdownMenu() {
  const editProject = useEditProject();

  return (
    <Dropdown
      key="header-dropdown"
      menu={{
        items: [
          { label: <DeleteButton />, key: 'delete-project' },
          editProject,
        ],
      }}
    >
      <FontAwesomeIcon className="cursor-pointer" icon={faEllipsisH} />
    </Dropdown>
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
      label={<div className="is-error">Delete</div>}
      okText="Delete"
      okType="error-light"
      onCancel={null}
      onConfirm={handleOnClick}
      title=" Are you sure you want to delete this project? "
    />
  );
}

const useEditProject = () => {
  const { uuid } = useParams();
  const { showModal } = useModals();

  const handleOnClick = async () => {
    showModal(ModalsEnum.EDIT_PROJECT, { uuid });
  };

  return (
    {
      label: 'Edit',
      onClick: handleOnClick,
      key: 'edit-project',
    }
  );
};

export default DropdownMenu;
