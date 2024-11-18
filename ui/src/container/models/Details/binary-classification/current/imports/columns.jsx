import { columnFactory } from '@Components/smart-table/utils';
import useModals from '@Hooks/use-modals';
import { JOB_STATUS, ModalsEnum } from '@Src/constants';
import { faExternalLink, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';
import moment from 'moment';
import { DataTableAction, FontAwesomeIcon, Spinner } from '@radicalbit/radicalbit-design-system';

export const getColumns = (activeFilters, activeSorter) => [
  columnFactory({
    title: 'File path',
    dataIndex: 'path',
    key: 'path',
    activeFilters,
    activeSorter,
  }),
  columnFactory({
    title: 'Imported at',
    dataIndex: 'date',
    key: 'date',
    activeFilters,
    activeSorter,
    sorter: true,
    render: (date) => moment(date).format('DD MMM YYYY HH:mm:ss').toString(),
  }),
  columnFactory({
    title: 'S',
    key: 'status',
    activeFilters,
    activeSorter,
    render: (data) => {
      switch (data.status) {
        case JOB_STATUS.IMPORTING:
          return (<Spinner spinning={data.status === JOB_STATUS.IMPORTING} />);

        case JOB_STATUS.ERROR:
          return (<FontAwesomeIcon icon={faTriangleExclamation} type="error" />);

        case JOB_STATUS.SUCCEEDED:
          return (<DataTableAction noHide><ImportActions data={data} /></DataTableAction>);

        default:
          return false;
      }
    },

  }),

];

function ImportActions({ data }) {
  const { showModal } = useModals();
  const showImportDetailModal = () => showModal(ModalsEnum.CURRENT_IMPORT_DETAIL, data);

  return (
    <div className="flex flex-row justify-end gap-2">
      <FontAwesomeIcon icon={faExternalLink} onClick={showImportDetailModal} />
    </div>
  );
}
