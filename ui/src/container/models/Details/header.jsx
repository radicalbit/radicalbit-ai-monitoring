import JobStatusTag from '@Components/JobStatus/job-status-tag';
import { STATUS_SELECTOR_MAX_LEN, TRUNCATE_LENGTH } from '@Src/constants';
import { DataTypeEnumLabel, GranularityEnumLabel, ModelTypeEnumLabel } from '@Src/store/state/models/constants';
import { modelsApiSlice } from '@State/models/api';
import { faEllipsisH } from '@fortawesome/free-solid-svg-icons';
import truncate from 'lodash/truncate';
import {
  Dropdown,
  FontAwesomeIcon,
  NewHeader, Popconfirm, RelativeDateTime, SectionTitle, StatusSelector,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { useNavigate, useParams } from 'react-router-dom';

const { useGetModelByUUIDQuery, useDeleteModelMutation } = modelsApiSlice;

export default function MainModelsHeader() {
  const { uuid } = useParams();

  const { data } = useGetModelByUUIDQuery({ uuid });
  const modelType = data?.modelType ? ModelTypeEnumLabel[data.modelType] : '--';
  const dataType = data?.dataType ? DataTypeEnumLabel[data.dataType] : '--';
  const granularity = data?.granularity ? GranularityEnumLabel[data.granularity] : '--';

  return (
    <NewHeader
      actions={{
        one: (
          <Dropdown
            key="header-dropdown"
            menu={{
              items: [
                { label: <DeleteButton />, key: 'delete-model' },
              ],
            }}
          >
            <FontAwesomeIcon className="cursor-pointer" icon={faEllipsisH} />
          </Dropdown>
        ),
      }}
      details={{
        one: (
          <>
            <StatusSelector
              status={{ current: modelType }}
              title="Model type"
            />

            <StatusSelector
              status={{ current: dataType }}
              title="Data type"
            />

            <Framework />

            <Algorithm />

            <StatusSelector
              status={{ current: granularity }}
              title="Granularity"
            />
          </>
        ),
      }}
      title={(
        <SectionTitle
          subtitle={<Subtitle />}
          title={<Title />}
          titleSuffix={<JobStatusTag />}
        />
      )}
    />
  );
}

function Title() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const name = data?.name;

  return name || '';
}

function Subtitle() {
  const { uuid } = useParams();
  const { data } = useGetModelByUUIDQuery({ uuid });

  const createdAt = data?.createdAt ?? 0;
  const updatedAt = data?.updatedAt ?? 0;

  return (
    <>
      {'Created: '}

      <RelativeDateTime threshold={3} timestamp={createdAt} withTooltip />

      {' • Updated: '}

      <RelativeDateTime threshold={3} timestamp={updatedAt} withTooltip />

    </>
  );
}

function Framework() {
  const { uuid } = useParams();

  const { data } = useGetModelByUUIDQuery({ uuid });
  const framework = data?.frameworks ?? '--';

  if (framework.length > STATUS_SELECTOR_MAX_LEN) {
    return (
      <StatusSelector
        status={{ current: <Tooltip title={framework}>{truncate(framework, { length: TRUNCATE_LENGTH })}</Tooltip> }}
        title="Framework"
      />
    );
  }

  return (
    <StatusSelector
      status={{ current: framework }}
      title="Framework"
    />
  );
}

function Algorithm() {
  const { uuid } = useParams();

  const { data } = useGetModelByUUIDQuery({ uuid });
  const algorithm = data?.algorithm ?? '--';

  if (algorithm.length > STATUS_SELECTOR_MAX_LEN) {
    return (
      <StatusSelector
        status={{ current: <Tooltip title={algorithm}>{truncate(algorithm, { length: TRUNCATE_LENGTH })}</Tooltip> }}
        title="Algorithm"
      />
    );
  }

  return (
    <StatusSelector
      status={{ current: algorithm }}
      title="Algorithm"
    />
  );
}

function DeleteButton() {
  const { uuid } = useParams();
  const navigate = useNavigate();

  const [triggerDeleteModel] = useDeleteModelMutation();
  const handleOnClick = async () => {
    const response = await triggerDeleteModel({ uuid });

    if (response.error) {
      console.error(response.error);
      return;
    }

    navigate('/models');
  };

  return (
    <Popconfirm
      label={<div className="is-error">Delete</div>}
      okText="Delete"
      okType="error-light"
      onCancel={null}
      onConfirm={handleOnClick}
      title=" Are you sure you want to delete this model? "
    />
  );
}
