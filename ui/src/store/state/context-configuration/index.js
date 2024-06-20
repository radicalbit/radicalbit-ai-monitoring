import contextConfigurationSelectors from './selectors';
import slice, { actions as contextConfigurationActions, initialState as contextConfigurationInitialState } from './slice';
import contextConfigurationThunks from './thunks';

export const selectors = { ...contextConfigurationSelectors };

export const actions = { ...contextConfigurationActions };

export const thunks = { ...contextConfigurationThunks };

export const initialState = { ...contextConfigurationInitialState };

export default slice;
