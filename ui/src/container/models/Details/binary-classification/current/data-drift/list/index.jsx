import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import { FEATURE_TYPE } from '@Container/models/Details/constants';
import {
  DRIFT_FEATURE_TYPE_ENUM,
  DRIFT_TEST_ENUM_LABEL, numberFormatter,
} from '@Src/constants';
import {
  Board,
  Button,
  FontAwesomeIcon,
  NewHeader,
  Pin,
  SectionTitle,
  Spinner,
  Tag,
} from '@radicalbit/radicalbit-design-system';
import { Virtuoso } from 'react-virtuoso';
import { fa1, faC } from '@fortawesome/free-solid-svg-icons';
import useGetFilteredFeatures from '../use-get-filtered-features';

function DataDriftList() {
  const items = useGetFilteredFeatures();

  if (items.length === 0) {
    return (<NoFeaturesAvailable />);
  }

  return (
    <Spinner fullHeight fullWidth>
      <Virtuoso
        data={items}
        itemContent={(idx, item) => (<FeatureRow key={idx} item={item} />)}
        totalCount={items.length}
      />
    </Spinner>
  );
}

function FeatureRow({ item }) {
  const driftAlgoritm = item?.driftCalc[0];

  const pinType = driftAlgoritm.hasDrift ? 'filled-error' : 'filled';
  const isError = driftAlgoritm.hasDrift ? 'is-error' : '';
  const value = driftAlgoritm.value > 0 ? numberFormatter().format(driftAlgoritm.value) : '--';
  const buttonIcon = getButtonIcon(item.fieldType);

  return (
    <Board
      key={item.featureName}
      header={(
        <NewHeader
          details={{
            one: (
              <div className="flex gap-4 justify-start">

                {DRIFT_TEST_ENUM_LABEL[driftAlgoritm.type]}

                <p className={`${isError} m-0`}>
                  <b className="font-[var(--coo-font-weight-bold)]">
                    {value}

                    {' '}
                  </b>

                </p>
              </div>
            ),
            two: (
              <Button
                shape="circle"
                size="small"
                type="primary"
              >
                <FontAwesomeIcon icon={buttonIcon} />
              </Button>
            ),
          }}
          title={(
            <div className="flex gap-2">
              <Pin type={pinType} />

              <SectionTitle
                size="small"
                title={item.featureName}
                titleSuffix={<Tag mode="text" type="secondary-light">{DRIFT_FEATURE_TYPE_ENUM[driftAlgoritm.type].toUpperCase()}</Tag>}
              />
            </div>
          )}
        />
      )}
      modifier="my-4 "
      size="small"
    />
  );
}

const getButtonIcon = (value) => {
  switch (value) {
    case FEATURE_TYPE.NUMERICAL:
      return fa1;

    case FEATURE_TYPE.CATEGORICAL:
      return faC;

    default:
      return '';
  }
};

export default DataDriftList;
