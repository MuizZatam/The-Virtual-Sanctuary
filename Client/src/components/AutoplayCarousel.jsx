import React from "react";
import './autoplaycarousel.css'
import { cardDetails } from "./carousel-config";

function AutoplayCarousel() {
  
  return (
    <div className="slider ">
      <div className="slide-track">
            {Object.keys(cardDetails).map((key) => (
                <div className="slide" key={key}>
                    <img src={cardDetails[key].imgUrl} alt={cardDetails[key].title} className="rounded-md"/>
                </div>
            ))}
            {Object.keys(cardDetails).map((key) => (
                <div className="slide" key={key}>
                    <img src={cardDetails[key].imgUrl} alt={cardDetails[key].title} className="rounded-md"/>
                </div>
            ))}      
        </div>
    </div>
  );
}

export default AutoplayCarousel;
