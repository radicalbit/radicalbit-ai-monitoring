import layoutSelectors from './selectors';
import slice, { actions as layoutActions } from './slice';

export const selectors = { ...layoutSelectors };

export const actions = { ...layoutActions };

export default slice;
