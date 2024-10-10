import { useNavigate } from 'react-router-dom';
import GetStartedButton from './GetStartedButton';

export default function TrialgetStarted() {
  const navigate = useNavigate();

  const handleClick = () => {
    // Add any additional logic here before navigation
    navigate('/demo');
  };

  return (
    <div>
      <button onClick={handleClick} className="">
        <GetStartedButton />
      </button>
    </div>
  );
}