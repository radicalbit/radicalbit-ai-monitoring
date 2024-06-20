import notificationSelectors from './selectors';
import slice, { actions as notificationActions } from './slice';

export const selectors = { ...notificationSelectors };

export const actions = { ...notificationActions };

export default slice;
