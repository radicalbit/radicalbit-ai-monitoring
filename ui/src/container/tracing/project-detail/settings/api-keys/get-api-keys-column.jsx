import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, Popconfirm, RelativeDateTime } from '@radicalbit/radicalbit-design-system';
import { columnFactory } from '@Src/components/smart-table/utils';
import { tracingApiSlice } from '@Src/store/state/tracing/api';
import { useParams } from 'react-router';

const { useDeleteApiKeyMutation, useAddNewApiKeyMutation } = tracingApiSlice;

const getApiKeyColumns = (
  activeFilters,
  activeSorter,
) => [

  columnFactory({
    title: 'Name',
    key: 'name',
    activeFilters,
    activeSorter,
    render: ({ name }) => (
      <div className="font-[var(--coo-font-weight-bold)]">
        {name}
      </div>
    ),
  }),

  columnFactory({
    title: 'Key',
    key: 'apiKey',
    dataIndex: 'apiKey',
    activeFilters,
    activeSorter,
  }),

  columnFactory({
    title: 'Created at',
    dataIndex: 'createdAt',
    key: 'createdAt',
    activeFilters,
    activeSorter,
    sorter: false,
    render: (date) => date && <RelativeDateTime timestamp={date} withTooltip />,
  }),

  columnFactory({
    title: '',
    key: 'uuid',
    activeFilters,
    activeSorter,
    sorter: false,
    render: (data) => <DeleteButton apiKeyName={data.name} />,
  }),

];

function DeleteButton({ apiKeyName }) {
  const { uuid } = useParams();
  const [triggerDeleteApiKey] = useDeleteApiKeyMutation();
  const [, args] = useAddNewApiKeyMutation({ fixedCacheKey: 'add-new-api-key' });

  const handleOnClick = async () => {
    const response = await triggerDeleteApiKey({ uuid, apiKeyName });

    if (response.error) {
      console.error(response.error);
    }
    args.reset();
  };

  return (
    <Popconfirm
      label={<FontAwesomeIcon icon={faTrash} type="error-light" />}
      okText="Delete"
      okType="error-light"
      onCancel={null}
      onConfirm={handleOnClick}
      title=" Are you sure you want to delete this API key? "
    />
  );
}

export default getApiKeyColumns;
