// src/components/OverlayDetail.js

import React from 'react';

const OverlayDetail = ({ type, item, onClose }) => {
  return (
    <div className="overlay">
      <div className="overlay-content">
        <button className="close-button" onClick={onClose}>
          X
        </button>
        {type === 'note' && (
          <div>
            <h3>Note Detail</h3>
            <p>{item.content}</p>
          </div>
        )}
        {type === 'task' && (
          <div>
            <h3>Task Detail</h3>
            <p>
              <strong>{item.title}</strong>
            </p>
            <p>Due Date: {item.dueDate}</p>
          </div>
        )}
        {type === 'habit' && (
          <div>
            <h3>Habit Detail</h3>
            <p>
              <strong>{item.name}</strong>
            </p>
            <p>Frequency: {item.frequency}</p>
          </div>
        )}
        <div className="future-actions">
          <button>AI Edit</button>
          <button>AI Suggestions</button>
        </div>
      </div>
    </div>
  );
};

export default OverlayDetail;
