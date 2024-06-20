import Logo from '@Img/logo.png';
import { Button, Void } from '@radicalbit/radicalbit-design-system';
import { useNavigate } from 'react-router-dom';

export default function NotFound() {
  const navigate = useNavigate();

  const handleOnClick = () => {
    navigate('/');
  };

  return (
    <Void
      actions={<Button onClick={handleOnClick} type="primary">Go To Home</Button>}
      description="We are sorry, the URL may be misspelled or the page you are looking for is no longer available"
      image={<img alt="Logo" src={Logo} />}
      title="Oh no, page not found"
    />
  );
}
