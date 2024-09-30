import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

const App = () => {
  const [speciesData, setSpeciesData] = useState({});
  const [loading, setLoading] = useState(false);
  const [audio, setAudio] = useState(null);
  const [location, setLocation] = useState(""); // No default location
  const [dataFetched, setDataFetched] = useState(false); // Track if data has been fetched

  // Fetch species data when the location is provided and submit button is clicked
  const fetchSpecies = async () => {
    if (!location) {
      alert("Please enter a location");
      return;
    }

    setLoading(true); // Start loading

    try {
      const response = await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ location }),
      });

      const data = await response.json();
      if (data.error) {
        console.error(data.error);
      } else {
        setSpeciesData(data.species_data);
        setDataFetched(true); // Mark data as fetched
      }
    } catch (error) {
      console.error('Error fetching species data:', error);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  // Play the audio associated with the species (on hover)
  const playAudio = (url) => {
    if (audio) {
      audio.pause(); // Pause existing audio if any
    }
    const newAudio = new Audio(url);
    setAudio(newAudio);
    newAudio.play();
  };

  const stopAudio = () => {
    if (audio) {
      audio.pause();
      setAudio(null);
    }
  };

  return (
    <div className="species-container">
      <h1>Species Information</h1>
      <input 
        type="text" 
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Enter location"
      />
      <button onClick={fetchSpecies}>Fetch Species</button>

      {loading && <p>Loading...</p>} {/* Show loading indicator */}

      {/* Render species cards only after data is fetched */}
      {dataFetched && Object.entries(speciesData).map(([species, data], index) => (
        <div key={index} className="species-card">
          <div className="species-card-left">
            {/* Display the first image in the left column */}
            {data.images.length > 0 && (
              <div className="image-container">
                <img
                  src={data.images[0]}
                  alt={data.inaturalist.name}
                  onMouseEnter={() => data.audio.length > 0 && playAudio(data.audio[0].url)}
                  onMouseLeave={stopAudio}
                  className="species-image"
                />
                {/* Display speaker emoji if audio is available */}
                {data.audio.length > 0 && (
                  <span className="speaker-icon">🔊</span>
                )}
              </div>
            )}
          </div>
          <div className="species-card-right">
            <h2>{data.inaturalist.name}</h2>
            <p><strong>Scientific Name:</strong> {data.inaturalist.scientific_name}</p>
            <p><strong>Observations Count:</strong> {data.inaturalist.observations_count}</p>
            <p><strong>Conservation Status:</strong> {data.inaturalist.conservation_status}</p>
            <ReactMarkdown>{data.wikipedia}</ReactMarkdown>
          </div>
        </div>
      ))}
    </div>
  );
};

export default App;
