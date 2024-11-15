const selectHasHeader = (state) => state.layout.hasHeader;
const selectHasLeftColumn = (state) => state.layout.hasLeftColumn;
const selectHasLeftColumnCollapsed = (state) => state.layout.hasLeftColumnCollapsed;

const selectHasHeaderContentDark = (state) => state.layout.hasHeaderContentDark;
const selectHasHeaderLeftContentDark = (state) => state.layout.hasHeaderLeftContentDark;
const selectHasHeaderRightContentDark = (state) => state.layout.hasHeaderRightContentDark;
const selectHasHeaderSecondaryContentDark = (state) => state.layout.hasHeaderSecondaryContentDark;
const selectHasLeftContentDark = (state) => state.layout.hasLeftContentDark;
const selectHasMainContentDark = (state) => state.layout.hasMainContentDark;
const selectHasRightContentDark = (state) => state.layout.hasRightContentDark;
const selectHasSecondaryContentDark = (state) => state.layout.hasSecondaryContentDark;

const selectHasRightColumn = (state) => state.layout.hasRightColumn;
const selectHasRightColumnCollapsed = (state) => state.layout.hasRightColumnCollapsed;
const selectHasSecondaryColumn = (state) => state.layout.hasSecondaryColumn;
const selectHasSecondaryColumnCollapsed = (state) => state.layout.hasSecondaryColumnCollapsed;
const selectShowBottomDrawerOnHover = (state) => state.layout.showBottomDrawerOnHover;

export default {
  selectHasHeader,
  selectHasHeaderContentDark,
  selectHasHeaderLeftContentDark,
  selectHasHeaderRightContentDark,
  selectHasHeaderSecondaryContentDark,
  selectHasLeftColumn,
  selectHasLeftColumnCollapsed,
  selectHasLeftContentDark,
  selectHasMainContentDark,
  selectHasRightColumn,
  selectHasRightColumnCollapsed,
  selectHasRightContentDark,
  selectHasSecondaryColumn,
  selectHasSecondaryColumnCollapsed,
  selectHasSecondaryContentDark,
  selectShowBottomDrawerOnHover,
};
