import './App.css'
import React, { useEffect, useState } from 'react'

function App() {
  const [formData, setFormData] = useState({
    location: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Sending form data to Flask backend
    fetch('http://localhost:5000/', {  // Changed from '/index' to '/'
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });

  };

  useEffect(() => {

    fetch('/')
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <>
      <form onSubmit={handleSubmit} id="formID">
        <input 
          type="text" 
          placeholder='Enter a Location' 
          name='location' 
          value={formData.location} 
          onChange={handleChange}
        />
        <input type="submit" />
      </form>
      
    </>
  )
}

export default App