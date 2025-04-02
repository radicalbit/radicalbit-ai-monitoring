import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import { FEATURE_TYPE } from '@Container/models/Details/constants';
import {
  fa1,
  faC,
  faChevronDown,
  faChevronUp,
} from '@fortawesome/free-solid-svg-icons';
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
import { useState } from 'react';
import { Virtuoso } from 'react-virtuoso';
import useGetFilteredFeatures from '../use-get-filtered-features';
import DetailDriftTable from './table';

function DataDriftList() {
  const items = useGetFilteredFeatures();

  if (items.length === 0) {
    return (<NoFeaturesAvailable />);
  }

  return (
    <Spinner fullHeight fullWidth>
      <Virtuoso
        data={items}
        itemContent={(idx, item) => (<DriftFeatureBoard key={idx} item={item} />)}
        totalCount={items.length}
      />
    </Spinner>
  );
}

function DriftFeatureBoard({ item }) {
  const [showDetail, setShowDetail] = useState(false);
  const hasDrift = item?.driftCalc.some((el) => el.hasDrift);

  const pinType = hasDrift ? 'filled-error' : 'filled';
  const buttonIcon = getButtonIcon(item.fieldType);

  const handleOnClick = () => {
    setShowDetail(!showDetail);
  };

  if (!showDetail) {
    return (
      <Board
        key={item.featureName}
        header={(
          <NewHeader
            details={{
              one: (
                <Button
                  shape="circle"
                  size="small"
                  type="primary"
                >
                  <FontAwesomeIcon icon={buttonIcon} />
                </Button>
              ),
              two: <FontAwesomeIcon icon={faChevronDown} />,
            }}
            title={(
              <div className="flex gap-4 ml-2">
                <Pin type={pinType} />

                <SectionTitle
                  size="small"
                  title={item.featureName}
                  titleSuffix={<Tag mode="text" type="secondary-light">{item.fieldType.toUpperCase()}</Tag>}
                />
              </div>
            )}
          />
        )}
        modifier="my-4 "
        onClick={handleOnClick}
        size="small"
      />
    );
  }

  return (
    <Board
      key={item.featureName}
      header={(
        <NewHeader
          details={{
            one: (
              <Button
                shape="circle"
                size="small"
                type="primary"
              >
                <FontAwesomeIcon icon={buttonIcon} />
              </Button>
            ),
            two: <FontAwesomeIcon icon={faChevronUp} />,
          }}
          title={(
            <div className="flex gap-4 ml-2">
              <Pin type={pinType} />

              <SectionTitle
                size="small"
                title={item.featureName}
                titleSuffix={<Tag mode="text" type="secondary-light">{item.fieldType.toUpperCase()}</Tag>}
              />
            </div>
          )}
        />
      )}
      main={(<DetailDriftTable data={item?.driftCalc} />)}
      modifier="my-4 "
      onClick={handleOnClick}
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
