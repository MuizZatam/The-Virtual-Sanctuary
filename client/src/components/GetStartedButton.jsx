import React from "react";
import upsideRightArrow from '../assets/upside-right-arrow.svg'
import { useNavigate } from 'react-router-dom';

function GetStartedButton() {
  const navigate = useNavigate();

  const handleClick = () => {
    // Add any additional logic here before navigation
    navigate('/demo');
  };
  return (
    <div >
      <button onClick={handleClick} 
        style={{ backgroundColor: "", color: "#ffffff", fontSize: "22px" }}
        className="flex font-medium max-w-[200px] ml-12  p-2.5 justify-between align-middle bg-blue-600 hover:bg-blue-500 items-center border rounded-xl "
      >
        <p>Get Started</p>
        <div className="mx-2">
          <img src={upsideRightArrow} alt="github-icon" />
        </div>
      </button>
      
    </div>
  );
}

export default GetStartedButton;
