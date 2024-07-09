import { FEATURE_TYPE } from '@Container/models/Details/constants';
import {
  fa1, faC,
} from '@fortawesome/free-solid-svg-icons';
import {
  Board,
  Button,
  FontAwesomeIcon,
  NewHeader,
  SectionTitle,
  Spinner,
  Tag,
} from '@radicalbit/radicalbit-design-system';
import { Virtuoso } from 'react-virtuoso';
import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import useGetFilteredFeatures from '../use-get-filtered-features';
import CategoricalLeftTable from './categorical/left-table/index';
import CategoricalRightTable from './categorical/right-table';
import NumericalBarChart from './numerical/chart/index';
import NumericalTable from './numerical/table/index';

function DataQualityList() {
  const items = useGetFilteredFeatures();

  if (items.length === 0) {
    return (<NoFeaturesAvailable />);
  }

  return (
    <Spinner className="mb-16" fullHeight fullWidth>
      <CountLabel />

      <Virtuoso
        data={items}
        itemContent={(index, item) => {
          switch (item.type) {
            case FEATURE_TYPE.NUMERICAL:
              return (<NumericalFeature key={index} item={item} />);

            case FEATURE_TYPE.CATEGORICAL:
              return (<CategoricalFeature key={index} item={item} />);

            default:
              return false;
          }
        }}
        totalCount={items.length}
      />
    </Spinner>
  );
}

function CountLabel() {
  const items = useGetFilteredFeatures();
  const label = items.length <= 1 ? 'Record' : 'Records';

  return (
    <label>
      {`${label} ${items.length}`}
    </label>
  );
}

function NumericalFeature({ item }) {
  const dataset = item?.histogram;

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
                <FontAwesomeIcon icon={fa1} />
              </Button>
            ),
          }}
          title={(
            <SectionTitle
              size="small"
              title={item.featureName}
              titleSuffix={<Tag mode="text" type="secondary-light">{item.type.toUpperCase()}</Tag>}
            />
        )}
        />
      )}
      main={(
        <div className="flex flex-col gap-4">

          <div className="flex flex-row gap-12">
            <div className="basis-2/5 ">
              <NumericalTable data={item} />
            </div>

            <div className="basis-3/5 ">
              <NumericalBarChart dataset={dataset} />
            </div>
          </div>

        </div>
      )}
      modifier="my-4 min-h-70"
      size="small"
    />
  );
}

function CategoricalFeature({ item }) {
  const dataset = item?.categoryFrequency ?? [];

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
                <FontAwesomeIcon icon={faC} />
              </Button>
            ),
          }}
          title={(
            <SectionTitle
              size="small"
              title={item.featureName}
              titleSuffix={<Tag mode="text" type="secondary-light">{item.type.toUpperCase()}</Tag>}
            />
        )}
        />
      )}
      main={(
        <div className="flex flex-col gap-4">
          <div className="flex flex-row gap-12">
            <div className="basis-2/5">
              <CategoricalLeftTable data={item} />
            </div>

            <div className="basis-3/5">
              <CategoricalRightTable data={dataset} />
            </div>
          </div>
        </div>
      )}
      modifier="my-4 min-h-70"
      size="small"
    />
  );
}

export default DataQualityList;
