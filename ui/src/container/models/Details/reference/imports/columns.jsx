import { columnFactory } from '@Components/smart-table/utils';
import { JOB_STATUS } from '@Src/constants';
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons';
import moment from 'moment';
import { FontAwesomeIcon, Spinner } from '@radicalbit/radicalbit-design-system';

export const getColumns = (activeFilters, activeSorter) => [
  columnFactory({
    title: 'File name',
    dataIndex: 'fileName',
    key: 'fileName',
    activeFilters,
    activeSorter,
  }),
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
    render: (date) => moment(date).format('DD MMM YYYY HH:mm:ss').toString(),
  }),
  columnFactory({
    title: '',
    key: 'status',
    dataIndex: 'status',
    activeFilters,
    activeSorter,
    render: (status) => {
      switch (status) {
        case JOB_STATUS.IMPORTING:
          return (<Spinner spinning={status === JOB_STATUS.IMPORTING} />);

        case JOB_STATUS.ERROR:
          return (<FontAwesomeIcon icon={faTriangleExclamation} type="error" />);

        default:
          return false;
      }
    },

  }),
];
