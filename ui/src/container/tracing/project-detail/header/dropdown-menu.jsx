import { faEllipsisH } from '@fortawesome/free-solid-svg-icons';
import { Dropdown, FontAwesomeIcon, Popconfirm } from '@radicalbit/radicalbit-design-system';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useNavigate, useParams } from 'react-router-dom';

const { useDeleteProjectMutation } = tracingApiSlice;

function DropdownMenu() {
  return (
    <Dropdown
      key="header-dropdown"
      menu={{
        items: [
          { label: <DeleteButton />, key: 'delete-project' },
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

export default DropdownMenu;
