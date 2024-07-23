import { FormField, Transfer } from '@radicalbit/radicalbit-design-system';
import { useModalContext } from '../modal-context-provider';

function FeatureTargetsLists() {
  return (<TransfertList />);
}

function TransfertList() {
  const { useFormbit, isMaximize } = useModalContext();
  const {
    form, error, write, writeAll,
  } = useFormbit;
  const variables = form?.variables;
  const featureKeys = form?.featureKeys;
  const outputKeys = form?.outputKeys;
  const dataSource = variables.map(({ name, type }) => ({ key: name, title: name, type }));

  const height = isMaximize ? 700 : 400;

  const filterOption = (inputValue, option) => option.title.indexOf(inputValue) > -1;

  const handleChange = (targetKeys, direction, keys) => {
    switch (direction) {
      case 'right': {
        write('featureKeys', featureKeys.filter((f) => !keys.includes(f)));
        break;
      }

      case 'left': {
        write('featureKeys', featureKeys.concat(keys));
        break;
      }

      default: break;
    }

    writeAll([
      ['outputKeys', targetKeys],
      ['__metadata.clearFieldNextStep', true],
    ]);
  };

  return (
    <>
      <Transfer
        dataSource={dataSource}
        filterOption={filterOption}
        headerType="light"
        onChange={handleChange}
        oneWay
        render={(item) => (
          <div className="flex flex-row gap-2">
            <div>{item.title}</div>

            <small>
              (
              {item.type}
              )
            </small>
          </div>
        )}
        showSearch
        style={{ height }}
        targetKeys={outputKeys}
        type="right-secondary"
      />

      {error('outputKeys') && <FormField message={error('outputKeys')} />}

      {error('featureKeys') && <FormField message={error('featureKeys')} />}
    </>
  );
}

export default FeatureTargetsLists;
