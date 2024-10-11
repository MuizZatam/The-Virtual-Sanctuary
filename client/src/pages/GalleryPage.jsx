import React, { useState, useEffect } from "react";
import "./Gallerypage.css";
import viewIcon from "../assets/view-icon.svg";
import Skeleton from "react-loading-skeleton";

function GalleryPage() {
  const [query, setQuery] = useState("koala");
  const [loading, setLoading] = useState();
  const [data, setData] = useState([]);

  const apiKey = import.meta.env.VITE_PEXELS_KEY;
  const getPictures = async () => {
    setLoading(true);
    await fetch(`https://api.pexels.com/v1/search?query=${query}`, {
      headers: {
        Authorization: apiKey,
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((res) => {
        setLoading(false);
        setData(res.photos);
      });
  };

  useEffect(() => {
    getPictures();
  }, []);

  const onKeyDownHandler = (e) => {
    if (e.keyCode === 13) {
      getPictures();
    }
  };

  return (
    <>
      {/* <div>API key: {apiKey}</div> */}
      <div>
        <div className="header">
          <div className="block text-4xl font-light">
            Explore a World of
            <span className="gradient font-extrabold">
              {" "}
              Wildlife and Flora
            </span>{" "}
            in through Stunning Images
          </div>
          <div className="block text-lg">
            <input
              className="inputSearch   min-h-10 p-2 m-2 mt-7 rounded-md text-gray-700"
              onKeyDown={onKeyDownHandler}
              placeholder="Search for Anything..."
              onChange={(e) => setQuery(e.target.value)}
              value={query}
            ></input>
          </div>
        </div>

        {loading && <h2></h2>}

        <div className="gallery mt-10">
          {data?.map((item, index) => {
            return (
              <div className="gallery-item ">
                <img src={item.src.medium} alt="" />
                <span>
                  <a
                    href={item.src.original}
                    download
                    className="download-button"
                    target="_blank"
                  >
                    <img src={viewIcon} className="view-icon" />
                  </a>
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

export default GalleryPage;
