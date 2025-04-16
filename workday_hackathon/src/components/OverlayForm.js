// components/OverlayForm.js

import React from 'react';

const OverlayForm = ({ type, onClose, onSubmit }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    // Convert form fields into an object.
    const data = {};
    formData.forEach((value, key) => (data[key] = value));
    onSubmit(data);
  };

  return (
    <div className="overlay">
      <div className="overlay-content">
        <button className="close-button" onClick={onClose}>
          X
        </button>
        <form onSubmit={handleSubmit}>
          <input type="hidden" name="type" value={type} />
          {type === 'note' && (
            <textarea name="content" placeholder="Enter note" required></textarea>
          )}
          {type === 'task' && (
            <>
              <input type="text" name="title" placeholder="Task Title" required />
              <input type="date" name="dueDate" required />
            </>
          )}
          {type === 'habit' && (
            <>
              <input type="text" name="name" placeholder="Habit Name" required />
              <select name="frequency" required>
                <option value="">Select Frequency</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </>
          )}
          <button type="submit">Save {type}</button>
        </form>
      </div>
    </div>
  );
};

export default OverlayForm;
