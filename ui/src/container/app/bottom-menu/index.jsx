import { ExternalPathsEnum } from '@Src/constants';
import { faCircleQuestion } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon, Menu } from '@radicalbit/radicalbit-design-system';

export default function BottomMenu() {
  const handleReadDocumentation = () => {
    window.open(`${ExternalPathsEnum.DOCUMENTATION}`, '_blank', 'noopener,noreferrer');
  };

  const items = [
    {
      key: 'Documentation',

      label: (
        <>
          <span className="anticon"><FontAwesomeIcon icon={faCircleQuestion} /></span>

          <span>Documentation</span>
        </>),
      onClick: handleReadDocumentation,
    },
  ];

  return (
    <Menu
      items={items}
      selectedKeys={undefined}
    />
  );
}
