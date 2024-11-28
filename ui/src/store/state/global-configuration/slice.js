import { createAction, createSlice } from '@reduxjs/toolkit';

const initialState = {
  showConfettiFroModelCreation: {},
};

const globalConfigurationActions = {
  addModelToShowConfettiList: createAction('ADD_MODEL_TO_SHOW_CONFETTI_LIST'),
  removeModelFromShowConfettiList: createAction('REMOVE_MODEL_FROM_SHOW_CONFETTI_LIST'),
};

export const globalConfigSlice = createSlice({
  name: 'global-config',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(
      globalConfigurationActions.addModelToShowConfettiList,
      (state, { payload }) => {
        state.showConfettiFroModelCreation = { ...state.showConfettiFroModelCreation, [payload]: true };
      },
    );
    builder.addCase(
      globalConfigurationActions.removeModelFromShowConfettiList,
      (state, { payload }) => {
        const { [payload]: _, ...other } = state.showConfettiFroModelCreation;
        state.showConfettiFroModelCreation = other;
      },
    );
  },
});

export const globalConfigSliceActions = {
  ...globalConfigSlice.actions,
  ...globalConfigurationActions,
};

export default globalConfigSlice.reducer;
