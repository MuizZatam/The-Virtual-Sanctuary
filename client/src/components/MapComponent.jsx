import React, { useEffect } from "react";
import mapboxgl from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css'; 

const MapComponent = () => {
  const mapboxToken = import.meta.env.VITE_MAPBOX_GL_TOKEN;

  useEffect(() => {
    if (mapboxToken) {
      mapboxgl.accessToken = mapboxToken;

      const map = new mapboxgl.Map({
        container: "map",
        center: [73.0910271, 19.2148599],
        zoom: 12, 
        attributionControl: false
      });

      map.addControl(
        new mapboxgl.AttributionControl({
          compact: true,
        }),
        "bottom-right"
      );

      return () => map.remove();
    } else {
      console.error("Mapbox token is missing or invalid");
    }
  }, [mapboxToken]);

  return (
    <div style={{display: "flex"}}>
      <div
        id="map"
        style={{
          justifyContent: "center",
          margin: "0px",
          width: "64em",
          height: "48em",
          border: "2px solid #fff",
          borderRadius: "5%"
        }}
      />
    </div>
  );
};

export default MapComponent;
