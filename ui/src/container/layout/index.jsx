import { PathsEnum } from '@Src/constants';
import { faRobot, faTachometer } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@radicalbit/radicalbit-design-system';
import { Link } from 'react-router-dom';

export const createRoutes = ({ currentPath }) => {
  const routeToCheck = currentPath.split('/')[1];
  const selectedItem = allRoutes.find(({ key }) => (routeToCheck === key))?.position;

  return { selectedItem, items: allRoutes };
};

const getLink = (pathname, search) => <Link to={{ pathname, search }} />;

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
];
