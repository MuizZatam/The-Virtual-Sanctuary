import React from "react";
import GetStarted from "./GetStartedButton";
import OneLiner from "./OneLiner";

function MainComponent() {
  return (
    <div className="flex justify-evenly items-center pt-24">
      <div className="left">
        
      </div>
      <div className="middle justify-center items-center block">
        <div className="">
          <OneLiner />
        </div>
        <div  className="flex justify-center items-center p-16">
          <GetStarted />
        </div>
      </div>

      <div className="right">
        
      </div>
    </div>
  );
}

export default MainComponent;
