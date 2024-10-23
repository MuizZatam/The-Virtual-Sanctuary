import React from "react";
import './OneLiner.css'
function OneLiner() {
  return (
    <>
      <div className="text-5xl font-light leading-tight text-center justify-center items-center">
        <i>
          <span className="font-medium ">Virtually Experience</span>
        </i>{" "}
        <br /> the rich biodiversity heritage <br /> that{" "}
        <i>
          <span className="font-extrabold one-liner" style={{}}>
            Mother Earth{" "}
          </span>
        </i>{" "}
        hosts!
      </div>
    </>
  );
}

export default OneLiner;
