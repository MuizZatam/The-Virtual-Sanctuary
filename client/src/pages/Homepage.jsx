import React from "react";
import "../App.css";

//components
import Header from "../components/Header";
import MainComponent from "../components/MainComponent";
import AutoplayCarousel from "../components/AutoplayCarousel";


function Homepage() {
  return (
    <>
      <div className="header">
        <Header />
      </div>
      <div className="main">
        <MainComponent />
      </div>
      <div className="auto-carousel"><AutoplayCarousel /></div>
    </>
  );
}

export default Homepage;
