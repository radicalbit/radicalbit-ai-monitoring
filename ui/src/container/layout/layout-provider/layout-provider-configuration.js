import { actions as layoutActions } from '@State/layout';

export const MAIN_LAYOUT_DARK_MODE_CONFIGURATION = [
  layoutActions.hideSecondaryColumn,
  layoutActions.darkenMainContent,
  layoutActions.darkenMainHeader,
  layoutActions.darkenRightColumn,
  layoutActions.darkenRightColumnHeader,
  layoutActions.darkenLeftColumn,
  layoutActions.darkenLeftColumnHeader,
  layoutActions.darkenSecondaryColumn,
  layoutActions.darkenSecondaryColumnHeader,
];

export const MAIN_LAYOUT_LIGHT_MODE_CONFIGURATION = [
  layoutActions.hideSecondaryColumn,
  layoutActions.lightenMainContent,
  layoutActions.lightenMainHeader,
  layoutActions.lightenRightColumn,
  layoutActions.lightenRightColumnHeader,
  layoutActions.lightenLeftColumn,
  layoutActions.lightenLeftColumnHeader,
  layoutActions.lightenSecondaryColumn,
  layoutActions.lightenSecondaryColumnHeader,
];

export const DETAIL_LAYOUT_DARK_MODE_CONFIGURATION = [
  layoutActions.showSecondaryColumn,
  layoutActions.darkenMainContent,
  layoutActions.darkenMainHeader,
  layoutActions.darkenRightColumn,
  layoutActions.darkenRightColumnHeader,
  layoutActions.darkenLeftColumn,
  layoutActions.darkenLeftColumnHeader,
  layoutActions.darkenSecondaryColumn,
  layoutActions.darkenSecondaryColumnHeader,
];

export const DETAIL_LAYOUT_LIGHT_MODE_CONFIGURATION = [
  layoutActions.showSecondaryColumn,
  layoutActions.lightenMainContent,
  layoutActions.lightenMainHeader,
  layoutActions.lightenRightColumn,
  layoutActions.lightenRightColumnHeader,
  layoutActions.lightenLeftColumn,
  layoutActions.lightenLeftColumnHeader,
  layoutActions.lightenSecondaryColumn,
  layoutActions.lightenSecondaryColumnHeader,
];

export const NOT_FOUND_CONFIGURATION = [
  layoutActions.hideHeader,
];
