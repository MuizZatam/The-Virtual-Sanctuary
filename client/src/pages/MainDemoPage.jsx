import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './MainDemoPage.css';
//skeleton
import Skeleton from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

const MainDemoPage = () => {
  const [speciesData, setSpeciesData] = useState({});
  const [loading, setLoading] = useState(false);
  const [audio, setAudio] = useState(null);
  const [location, setLocation] = useState(""); // No default location
  const [dataFetched, setDataFetched] = useState(false); // Track if data has been fetched
  const [narrating, setNarrating] = useState({}); // Track narration state for each species

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
        setNarrating({}); // Reset narration state
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

  // Strip markdown syntax from text (so it narrates plain text)
  const stripMarkdown = (markdown) => {
    return markdown
      .replace(/[#*_>\[\]]+/g, '') // Remove markdown symbols like #, *, _ and links
      .replace(/\(.*?\)/g, ''); // Remove URLs or parenthesis content
  };

  // Narrate markdown text
  const narrateText = (species, text) => {
    const speech = new SpeechSynthesisUtterance(stripMarkdown(text));
    
    speech.onend = () => {
      setNarrating((prev) => ({ ...prev, [species]: false }));
    };

    window.speechSynthesis.speak(speech);
    setNarrating((prev) => ({ ...prev, [species]: true }));
  };

  // Stop the narration
  const stopNarration = (species) => {
    window.speechSynthesis.cancel();
    setNarrating((prev) => ({ ...prev, [species]: false }));
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

      {loading &&  <Skeleton  highlightColor="#435"/>} {/* Show loading indicator */}

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

            {/* Play/Pause button for narration */}
            <button 
              className="narration-btn"
              onClick={() => narrating[species] 
                ? stopNarration(species) 
                : narrateText(species, data.wikipedia)}
            >
              {narrating[species] ? 'Pause' : 'Play'} Narration
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MainDemoPage;
