import { createAction, createSlice } from '@reduxjs/toolkit';

const initialState = {
  hasHeaderLeftContentDark: false,
  hasLeftContentDark: false,

  hasHeaderRightContentDark: false,
  hasHeader: true,
  hasHeaderContentDark: true,
  hasHeaderSecondaryContentDark: true,
  hasLeftColumn: true,
  hasLeftColumnCollapsed: true,
  hasMainContentDark: true,
  hasRightColumn: false,
  hasRightColumnCollapsed: false,
  hasRightContentDark: false,
  hasSecondaryColumn: false,
  hasSecondaryColumnCollapsed: false,
  hasSecondaryContentDark: true,
  isAllDark: false,
  showBottomDrawerOnHover: false,
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
    builder.addCase(layoutActions.collapseLeftColumn, (state) => ({ ...state, hasLeftColumnCollapsed: true }));

    builder.addCase(layoutActions.darkenMainContent, (state) => ({ ...state, hasMainContentDark: true }));
    builder.addCase(layoutActions.darkenMainHeader, (state) => ({ ...state, hasHeaderContentDark: true }));
    builder.addCase(layoutActions.darkenRightColumn, (state) => ({ ...state, hasHeaderRightContentDark: true }));
    builder.addCase(layoutActions.darkenRightColumnHeader, (state) => ({ ...state, hasHeaderRightContentDark: true }));
    builder.addCase(layoutActions.darkenLeftColumn, (state) => ({ ...state, hasLeftContentDark: true }));
    builder.addCase(layoutActions.darkenLeftColumnHeader, (state) => ({ ...state, hasHeaderLeftContentDark: true }));
    builder.addCase(layoutActions.darkenSecondaryColumn, (state) => ({ ...state, hasSecondaryContentDark: true }));
    builder.addCase(layoutActions.darkenSecondaryColumnHeader, (state) => ({ ...state, hasHeaderSecondaryContentDark: true }));

    builder.addCase(layoutActions.expandLeftColumn, (state) => ({ ...state, hasLeftColumnCollapsed: false }));
    builder.addCase(layoutActions.hideHeader, (state) => ({ ...state, hasHeader: false }));
    builder.addCase(layoutActions.hideRightColumn, (state) => ({ ...state, hasLeftColumnCollapsed: false }));
    builder.addCase(layoutActions.hideSecondaryColumn, (state) => ({ ...state, hasSecondaryColumn: false }));

    builder.addCase(layoutActions.lightenMainContent, (state) => ({ ...state, hasMainContentDark: false }));
    builder.addCase(layoutActions.lightenMainHeader, (state) => ({ ...state, hasHeaderContentDark: false }));
    builder.addCase(layoutActions.lightenRightColumn, (state) => ({ ...state, hasHeaderRightContentDark: false }));
    builder.addCase(layoutActions.lightenRightColumnHeader, (state) => ({ ...state, hasHeaderRightContentDark: false }));
    builder.addCase(layoutActions.lightenLeftColumn, (state) => ({ ...state, hasLeftContentDark: false }));
    builder.addCase(layoutActions.lightenLeftColumnHeader, (state) => ({ ...state, hasHeaderLeftContentDark: false }));
    builder.addCase(layoutActions.lightenSecondaryColumn, (state) => ({ ...state, hasSecondaryContentDark: false }));
    builder.addCase(layoutActions.lightenSecondaryColumnHeader, (state) => ({ ...state, hasHeaderSecondaryContentDark: false }));

    builder.addCase(layoutActions.showHeader, (state) => ({ ...state, hasHeader: true }));
    builder.addCase(layoutActions.showLeftColumn, (state) => ({ ...state, hasLeftColumn: true }));
    builder.addCase(layoutActions.showRightColumn, (state) => ({ ...state, hasRightColumn: true }));
    builder.addCase(layoutActions.showSecondaryColumn, (state) => ({ ...state, hasSecondaryColumn: true }));
    builder.addCase(layoutActions.toggleCollapseLeftColumn, (state) => ({ ...state, hasLeftColumnCollapsed: !state.hasLeftColumnCollapsed }));
    builder.addCase(layoutActions.toggleCollapseSecondaryColumn, (state) => ({ ...state, hasSecondaryColumnCollapsed: !state.hasSecondaryColumnCollapsed }));
  },
});

export const actions = {
  ...layoutSlice.actions,
  ...layoutActions,
};

export default layoutSlice.reducer;
