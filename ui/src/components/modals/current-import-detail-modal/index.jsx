import useModals from '@Hooks/use-modals';
import { STATUS_SELECTOR_MAX_LEN, TRUNCATE_LENGTH } from '@Src/constants';
import { modelsApiSlice } from '@State/models/api';
import { DataTypeEnumLabel, GranularityEnumLabel, ModelTypeEnumLabel } from '@State/models/constants';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons';
import { truncate } from 'lodash';
import moment from 'moment';
import {
  FontAwesomeIcon,
  NewHeader,
  RbitModal,
  SectionTitle,
  StatusSelector,
  Tooltip,
} from '@radicalbit/radicalbit-design-system';
import { memo } from 'react';
import { useParams } from 'react-router-dom';
import { useSearchParams } from 'react-router-dom';
import Body from './body';

const { useGetModelByUUIDQuery } = modelsApiSlice;

function CurrentImportDetailModal() {
  const { hideModal } = useModals();
  const [searchParams, setSearchParams] = useSearchParams();

  const handleOnCancel = () => {
    searchParams.delete('modal-tab-metrics');
    setSearchParams(searchParams);
    hideModal();
  };

  return (
    <RbitModal
      header={<Header />}
      headerType="light"
      maximize
      onCancel={handleOnCancel}
      open
    >
      <Body />
    </RbitModal>
  );
}

function Header() {
  const { uuid } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const { hideModal, modalPayload: { data } } = useModals();

  const { data: model } = useGetModelByUUIDQuery({ uuid });
  const modelType = model?.modelType ? ModelTypeEnumLabel[model.modelType] : '--';
  const dataType = model?.dataType ? DataTypeEnumLabel[model.dataType] : '--';
  const granularity = model?.granularity ? GranularityEnumLabel[model.granularity] : '--';

  const splittedPath = data?.path.split('/') ?? [];
  const fileName = splittedPath.length > 0 ? splittedPath[splittedPath.length - 1] : '';

  const updateTime = data?.date ?? '';
  const subtitle = `updated at ${moment(updateTime).format('DD MMM YYYY HH:mm:ss').toString()}`;

  const handleOnCancel = () => {
    searchParams.delete('modal-tab-metrics');
    setSearchParams(searchParams);
    hideModal();
  };

  return (
    <NewHeader
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
      prefix={<FontAwesomeIcon enableColorMode icon={faArrowLeft} onClick={handleOnCancel} />}
      title={(
        <SectionTitle
          subtitle={subtitle}
          title={fileName}
        />
      )}
    />
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
export default memo(CurrentImportDetailModal);
