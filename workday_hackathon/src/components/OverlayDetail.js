// src/components/OverlayDetail.js
import React, { useState } from 'react';

const OverlayDetail = ({ type, item, onClose }) => {
  const [aiResult, setAiResult] = useState("");

  // Helper function to build a text block from the item details.
  const getItemText = () => {
    if (type === 'note') return item.content;
    if (type === 'task') return `Task Title: ${item.title}\nDue Date: ${item.dueDate}`;
    if (type === 'habit') return `Habit Name: ${item.name}\nFrequency: ${item.frequency}`;
    return "";
  };

  const handleAiEdit = async () => {
    try {
      const response = await fetch("http://localhost:000/api/ai_edit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: getItemText() }),
      });
      const data = await response.json();
      setAiResult(data.response);
    } catch (error) {
      console.error("Error calling AI Edit:", error);
    }
  };

  const handleAiSuggestions = async () => {
    try {
      const response = await fetch("http://localhost:3000/api/ai_suggestions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: getItemText() }),
      });
      const data = await response.json();
      setAiResult(data.response);
    } catch (error) {
      console.error("Error calling AI Suggestions:", error);
    }
  };

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
          <button onClick={handleAiEdit}>AI Edit</button>
          <button onClick={handleAiSuggestions}>AI Suggestions</button>
        </div>
        {aiResult && (
          <div className="ai-result">
            <h4>AI Response:</h4>
            <p>{aiResult}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default OverlayDetail;
