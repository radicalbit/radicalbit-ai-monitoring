import { actions as layoutActions } from '@State/layout';

export const MAIN_LAYOUT_CONFIGURATION = [
  layoutActions.hideSecondaryColumn,
  layoutActions.darkenMainContent,
  layoutActions.darkenMainHeader,
  layoutActions.showHeader,
];

export const DETAIL_LAYOUT_CONFIGURATION = [
  layoutActions.showSecondaryColumn,
  layoutActions.darkenMainContent,
  layoutActions.darkenMainHeader,
  layoutActions.showHeader,
];

export const DARK_MODE_CONFIGURATION = [
  layoutActions.darkenMainContent,
  layoutActions.darkenMainHeader,
  layoutActions.darkenRightColumn,
  layoutActions.darkenRightColumnHeader,
  layoutActions.darkenLeftColumn,
  layoutActions.darkenLeftColumnHeader,
  layoutActions.darkenSecondaryColumn,
  layoutActions.darkenSecondaryColumnHeader,
];

export const LIGHTEN_DETAIL_MODE_CONFIGURATION = [
  layoutActions.lightenMainContent,
  layoutActions.lightenMainHeader,
  layoutActions.lightenRightColumn,
  layoutActions.lightenRightColumnHeader,
  layoutActions.lightenLeftColumn,
  layoutActions.lightenLeftColumnHeader,
  layoutActions.darkenSecondaryColumn,
  layoutActions.darkenSecondaryColumnHeader,

];

export const NOT_FOUND_CONFIGURATION = [
  layoutActions.hideHeader,
];
