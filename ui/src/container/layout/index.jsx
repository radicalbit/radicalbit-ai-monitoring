import { PathsEnum } from '@Src/constants';
import { faRobot, faTachometer } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@radicalbit/radicalbit-design-system';
import { Link } from 'react-router-dom';

export const createRoutes = ({ currentPath, isProjectTracingEnabled }) => {
  const routeToCheck = currentPath.split('/')[1];

  const items = isProjectTracingEnabled ? allRoutes : allRoutes.filter((route) => route.key !== PathsEnum.TRACING_PROJECT);

  const selectedItem = items.find(({ key }) => (routeToCheck === key))?.position;

  return { selectedItem, items };
};

const getLink = (pathname, search) => <Link to={{ pathname, search }}><div className="hidden">{pathname}</div></Link>;

const allRoutes = [
  {
    position: 1,
    title: 'Launchpad',
    icon: <FontAwesomeIcon icon={faTachometer} />,
    key: PathsEnum.LAUNCHPAD,
    link: getLink(`/${PathsEnum.LAUNCHPAD}`),
    visibility: [],
  },
  {
    position: 2,
    title: 'Models',
    icon: <FontAwesomeIcon icon={faRobot} />,
    key: PathsEnum.MODELS,
    link: getLink(`/${PathsEnum.MODELS}`),
    visibility: [],
  },
  {
    position: 3,
    title: 'Tracing',
    icon: <FontAwesomeIcon icon={faRobot} />,
    key: PathsEnum.TRACING_PROJECT,
    link: getLink(`/${PathsEnum.TRACING_PROJECT}`),
    visibility: [],
  },
];
