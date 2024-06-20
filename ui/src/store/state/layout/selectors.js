const selectHasHeader = (state) => state.layout.hasHeader;
const selectHasLeftColumn = (state) => state.layout.hasLeftColumn;
const selectHasLeftColumnCollapsed = (state) => state.layout.hasLeftColumnCollapsed;
const selectHasMainContentDark = (state) => state.layout.hasMainContentDark;
const selectHasRightColumn = (state) => state.layout.hasRightColumn;
const selectHasRightColumnCollapsed = (state) => state.layout.hasRightColumnCollapsed;
const selectHasRightContentDark = (state) => state.layout.hasRightContentDark;
const selectHasSecondaryColumn = (state) => state.layout.hasSecondaryColumn;
const selectHasSecondaryColumnCollapsed = (state) => state.layout.hasSecondaryColumnCollapsed;
const selectHasSecondaryContentDark = (state) => state.layout.hasSecondaryContentDark;
const selectHasHeaderSecondaryContentDark = (state) => state.layout.hasHeaderSecondaryContentDark;
const selectIsAllDark = (state) => state.layout.isAllDark;
const selectShowBottomDrawerOnHover = (state) => state.layout.showBottomDrawerOnHover;
const selectHasHeaderContentDark = (state) => state.layout.hasHeaderContentDark;

export default {
  selectHasLeftColumnCollapsed,
  selectHasRightColumnCollapsed,
  selectHasSecondaryColumnCollapsed,
  selectHasRightColumn,
  selectHasLeftColumn,
  selectHasSecondaryColumn,
  selectHasHeader,
  selectHasRightContentDark,
  selectHasMainContentDark,
  selectHasSecondaryContentDark,
  selectHasHeaderSecondaryContentDark,
  selectShowBottomDrawerOnHover,
  selectIsAllDark,
  selectHasHeaderContentDark,
};
