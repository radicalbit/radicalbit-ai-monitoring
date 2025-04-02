import { Pin } from '@radicalbit/radicalbit-design-system';
import { DRIFT_TEST_ENUM_LABEL, numberFormatter } from '@Src/constants';

const columns = [
  {
    key: 'hasDrift',
    dataIndex: 'hasDrift',
    width: '1px',
    render: (hasDrift) => {
      const pinType = hasDrift ? 'filled-error' : 'filled';
      return (
        <Pin type={pinType} />
      );
    },
  },
  {
    title: 'Algorithm',
    key: 'type',
    dataIndex: 'type',
    render: (type) => DRIFT_TEST_ENUM_LABEL[type],
  },
  {
    title: 'Threshold',
    key: 'limit',
    dataIndex: 'limit',
    width: '6rem',
    render: (value) => numberFormatter().format(value),
  },
  {
    title: 'Value',
    key: 'value',
    dataIndex: 'value',
    width: '6rem',
    render: (value) => `${value}`.includes('e') ? Number.parseFloat(value).toExponential(2) : numberFormatter().format(value),
  },
];

export default columns;
