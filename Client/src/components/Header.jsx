import React from "react";
import { Link } from "react-router-dom";
import Contribute from "./Contribute";
import tvsIcon from "../assets/tvs-icon.svg";



export default function Header() {

  const openWhenClicked = () => {
    window.open('https://github.com/MuizZatam/The-Virtual-Sanctuary', '_blank'); // '_blank' opens in a new tab
  };

  return (
    <div className="max-h-20 sticky flex  justify-evenly items-center text-xl">
      <div className="left flex  justify-between items-center">
        <div>
          <img src={tvsIcon} alt="" />
        </div>
      </div>
      <div className="right flex  justify-evenly items-center">
        {/* <div>Ask Us</div> */}
        <div className="px-10">
          <Link to="/gallery">Gallery</Link>
        </div>
        {/* <div>Team</div> */}
        <div onClick={openWhenClicked}>
          <Contribute />
        </div>
      </div>
    </div>
  );
}
