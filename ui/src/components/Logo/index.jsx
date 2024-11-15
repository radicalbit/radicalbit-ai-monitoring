import LogoSquared from '@Img/logo-collapsed.svg';
import LogoExpandedForDark from '@Img/logo-expanded-neg.svg';
import LogoExpandedForLight from '@Img/logo-expanded-pos.svg';
import { selectors as layoutSelectors } from '@State/layout';
import { useSelector } from 'react-redux';

const {
  selectHasLeftColumnCollapsed,
  selectHasHeaderLeftContentDark,
} = layoutSelectors;

export default function Logo({ className = '', onClick, title }) {
  const hasLeftColumnCollapsed = useSelector(selectHasLeftColumnCollapsed);
  const hasHeaderLeftContentDark = useSelector(selectHasHeaderLeftContentDark);

  const shape = hasLeftColumnCollapsed ? 'collapsed' : 'expanded';
  const color = hasHeaderLeftContentDark ? 'dark' : 'light';

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
      className={`${className} p-4`}
      onClick={onClick}
      role="presentation"
      title={title}
    >
      {svg}
    </a>
  );
}
