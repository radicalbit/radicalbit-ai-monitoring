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

export const NOT_FOUND_CONFIGURATION = [
  layoutActions.hideHeader,
];
