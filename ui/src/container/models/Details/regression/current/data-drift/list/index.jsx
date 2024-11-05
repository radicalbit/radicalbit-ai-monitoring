import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import { FEATURE_TYPE } from '@Container/models/Details/constants';
import {
  DRIFT_FEATURE_TYPE_ENUM,
  DRIFT_TEST_ENUM_LABEL, numberFormatter,
} from '@Src/constants';
import { fa1, faC } from '@fortawesome/free-solid-svg-icons';
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
  const pinType = (item.driftCalc.hasDrift) ? 'filled-error' : 'filled';
  const isError = (item.driftCalc.hasDrift) ? 'is-error' : '';
  const value = (item.driftCalc.value > 0) ? numberFormatter().format(item.driftCalc.value) : '--';
  const buttonIcon = getButtonIcon(item.fieldType);

  return (
    <Board
      key={item.featureName}
      header={(
        <NewHeader
          details={{
            one: (
              <div className="flex gap-4 justify-start">

                {DRIFT_TEST_ENUM_LABEL[item.driftCalc.type]}

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
                titleSuffix={<Tag mode="text" type="secondary-light">{DRIFT_FEATURE_TYPE_ENUM[item.driftCalc.type].toUpperCase()}</Tag>}
              />
            </div>
          )}
        />
      )}
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
