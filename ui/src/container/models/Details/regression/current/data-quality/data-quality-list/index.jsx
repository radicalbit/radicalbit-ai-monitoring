import NoFeaturesAvailable from '@Components/ErrorPage/no-features';
import { FEATURE_TYPE } from '@Container/models/Details/constants';
import {
  Board,
  Button,
  NewHeader,
  SectionTitle,
  Spinner,
  Tag,
} from '@radicalbit/radicalbit-design-system';
import { Virtuoso } from 'react-virtuoso';
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

      />
    </Spinner>
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
                <span className="mt-1">1</span>
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
      modifier="my-4 h-[20rem]"
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
                <span className="mt-1">C</span>
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

            <div className="basis-3/5 ">
              <CategoricalRightTable data={dataset} />
            </div>
          </div>
        </div>
      )}
      modifier="my-4 h-[20rem]"
      size="small"
    />
  );
}

export default DataQualityList;
