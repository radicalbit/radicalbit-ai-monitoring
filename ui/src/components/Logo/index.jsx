import LogoSquared from '@Img/logo-collapsed.svg';
import LogoExpandedForDark from '@Img/logo-expanded-neg.svg';
import LogoExpandedForLight from '@Img/logo-expanded-pos.svg';
import { selectors as layoutSelectors } from '@State/layout';
import { useSelector } from 'react-redux';

const {
  selectHasLeftColumnCollapsed,
  selectIsAllDark,
} = layoutSelectors;

export default function Logo({ onClick, title }) {
  const hasLeftColumnCollapsed = useSelector(selectHasLeftColumnCollapsed);
  const isAllDark = useSelector(selectIsAllDark);

  const shape = hasLeftColumnCollapsed ? 'collapsed' : 'expanded';
  const color = isAllDark ? 'light' : 'dark';

  const logos = {
    expanded: {
      light: <LogoExpandedForLight />,
      dark: <LogoExpandedForDark />,
    },
    collapsed: {
      light: <LogoSquared />,
      dark: <LogoSquared />,
    },
  };

  const svg = logos[shape][color];

  return (
    <a
      onClick={onClick}
      role="presentation"
      title={title}
    >
      {svg}
    </a>
  );
}
