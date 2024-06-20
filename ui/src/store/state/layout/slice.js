import { createAction, createSlice } from '@reduxjs/toolkit';

const initialState = {
  hasHeader: true,
  hasLeftColumn: true,
  hasLeftColumnCollapsed: true,
  hasMainContentDark: true,
  hasRightColumn: false,
  hasRightColumnCollapsed: false,
  hasRightContentDark: false,
  hasSecondaryColumn: false,
  hasSecondaryColumnCollapsed: false,
  hasSecondaryContentDark: true,
  hasHeaderSecondaryContentDark: true,
  isAllDark: false,
  showBottomDrawerOnHover: false,
  hasHeaderContentDark: true,
};

const layoutActions = {
  collapseLeftColumn: createAction('COLLAPSE_LEFT_COLUMN'),
  darkenMainContent: createAction('DARKEN_MAIN_CONTENT'),
  darkenMainHeader: createAction('DARKEN_MAIN_HEADER'),
  darkenRightColumn: createAction('DARKEN_RIGHT_COLUMN'),
  expandLeftColumn: createAction('EXPAND_LEFT_COLUMN'),
  hideHeader: createAction('HIDE_HEADER'),
  hideRightColumn: createAction('HIDE_RIGHT_COLUMN'),
  hideSecondaryColumn: createAction('HIDE_SECONDARY_COLUMN'),
  lightenMainContent: createAction('LIGHTEN_MAIN_CONTENT'),
  lightenMainHeader: createAction('LIGHTEN_MAIN_HEADER'),
  showHeader: createAction('SHOW_HEADER'),
  showLeftColumn: createAction('SHOW_LEFT_COLUMN'),
  showRightColumn: createAction('SHOW_RIGHT_COLUMN'),
  showSecondaryColumn: createAction('SHOW_SECONDARY_COLUMN'),
  toggleCollapseLeftColumn: createAction('TOGGLE_COLLAPSE_LEFT_COLUMN'),
  toggleCollapseSecondaryColumn: createAction('TOGGLE_COLLAPSE_SECONDARY_COLUMN'),
};

export const layoutSlice = createSlice({
  name: 'layout',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(layoutActions.toggleCollapseSecondaryColumn, (state) => ({ ...state, hasSecondaryColumnCollapsed: !state.hasSecondaryColumnCollapsed }));

    builder.addCase(layoutActions.toggleCollapseLeftColumn, (state) => ({ ...state, hasLeftColumnCollapsed: !state.hasLeftColumnCollapsed }));

    builder.addCase(layoutActions.expandLeftColumn, (state) => ({ ...state, hasLeftColumnCollapsed: false }));

    builder.addCase(layoutActions.collapseLeftColumn, (state) => ({ ...state, hasLeftColumnCollapsed: true }));

    builder.addCase(layoutActions.showHeader, (state) => ({ ...state, hasHeader: true }));

    builder.addCase(layoutActions.showLeftColumn, (state) => ({ ...state, hasLeftColumn: true }));

    builder.addCase(layoutActions.showRightColumn, (state) => ({ ...state, hasRightColumn: true }));

    builder.addCase(layoutActions.showSecondaryColumn, (state) => ({ ...state, hasSecondaryColumn: true }));

    builder.addCase(layoutActions.hideHeader, (state) => ({ ...state, hasHeader: false }));

    builder.addCase(layoutActions.hideRightColumn, (state) => ({ ...state, hasLeftColumnCollapsed: false }));

    builder.addCase(layoutActions.hideSecondaryColumn, (state) => ({ ...state, hasSecondaryColumn: false }));

    builder.addCase(layoutActions.darkenRightColumn, (state) => ({ ...state, hasRightContentDark: false }));

    builder.addCase(layoutActions.darkenMainContent, (state) => ({ ...state, hasMainContentDark: true, hasRightContentDark: true }));

    builder.addCase(layoutActions.darkenMainHeader, (state) => ({ ...state, hasHeaderContentDark: true }));

    builder.addCase(layoutActions.lightenMainContent, (state) => ({ ...state, hasMainContentDark: false }));

    builder.addCase(layoutActions.lightenMainHeader, (state) => ({ ...state, hasHeaderContentDark: false }));
  },
});

export const actions = {
  ...layoutSlice.actions,
  ...layoutActions,
};

export default layoutSlice.reducer;
