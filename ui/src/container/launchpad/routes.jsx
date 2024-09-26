import { PathsEnum } from '@Src/constants';
import Launchpad from '.';

export const launchpadRoutes = {
  path: `${PathsEnum.LAUNCHPAD}`,
  children: [
    { path: '', element: <Launchpad /> },
  ],
};
