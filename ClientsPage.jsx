import React, { useState } from 'react';
import './ClientsPage.css';

function ClientsPage() {
  const [formData, setFormData] = useState({
    name: '',
    need: '',
    location: '',
    gender: '',
    language: '',
    cultural_background: '',
    preferred_gender: '',
    preferred_cultural_background: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData); // This will display the inputted data in the console for now
  };

  return (
    <div className="ClientsPage">
      <form className="form-container" onSubmit={handleSubmit}>
        <h2>Client Information</h2>
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Need:
          <input
            type="text"
            name="need"
            value={formData.need}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Location:
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Gender:
          <input
            type="text"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Language:
          <input
            type="text"
            name="language"
            value={formData.language}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Cultural Background:
          <input
            type="text"
            name="cultural_background"
            value={formData.cultural_background}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Preferred Gender:
          <input
            type="text"
            name="preferred_gender"
            value={formData.preferred_gender}
            onChange={handleChange}
          />
        </label>

        <label>
          Preferred Cultural Background:
          <input
            type="text"
            name="preferred_cultural_background"
            value={formData.preferred_cultural_background}
            onChange={handleChange}
          />
        </label>

        <button type="submit" className="custom-button">Submit</button>
      </form>
    </div>
  );
}

export default ClientsPage;
