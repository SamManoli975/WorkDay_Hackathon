// src/components/OverlayDetail.js
import React, { useState } from 'react';

const OverlayDetail = ({ type, item, onClose }) => {
  const [aiResult, setAiResult] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Helper function to build a text block from the item details.
  const getItemText = () => {
    if (type === 'note') return item.content;
    if (type === 'task') return `Task Title: ${item.title}\nDue Date: ${item.dueDate}`;
    if (type === 'habit') return `Habit Name: ${item.name}\nFrequency: ${item.frequency}`;
    return "";
  };

  const handleAiEdit = async () => {
    setIsLoading(true);
    setError("");
    
    try {
      const response = await fetch("http://localhost:5000/api/ai_edit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: getItemText() }),
      });
      
      

      // First check if the response is ok
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      // Get response text first to debug
      const rawText = await response.text();
      
      // Try parsing the response as JSON
      let data;
      try {
        data = JSON.parse(rawText);
      } catch (parseError) {
        console.error("Failed to parse JSON:", parseError);
        console.error("Raw response:", rawText);
        throw new Error(`Invalid JSON response: ${rawText.substring(0, 100)}...`);
      }

      // Check if data has the expected structure
      if (!data || typeof data.response === 'undefined') {
        throw new Error(`Unexpected response format: ${JSON.stringify(data)}`);
      }

      setAiResult(data.response);
    } catch (error) {
      console.error("Error calling AI Edit:", error);
      setError(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAiSuggestions = async () => {
    setIsLoading(true);
    setError("");
    
    try {
      const response = await fetch("http://localhost:5000/api/ai_suggestions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: getItemText() }),
      });
      

      // First check if the response is ok
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      // Get response text first to debug
      const rawText = await response.text();
      
      // Try parsing the response as JSON
      let data;
      try {
        data = JSON.parse(rawText);
      } catch (parseError) {
        console.error("Failed to parse JSON:", parseError);
        console.error("Raw response:", rawText);
        throw new Error(`Invalid JSON response: ${rawText.substring(0, 100)}...`);
      }

      // Check if data has the expected structure
      if (!data || typeof data.response === 'undefined') {
        throw new Error(`Unexpected response format: ${JSON.stringify(data)}`);
      }

      setAiResult(data.response);
    } catch (error) {
      console.error("Error calling AI Suggestions:", error);
      setError(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
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
          <button onClick={handleAiEdit} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'AI Edit'}
          </button>
          <button onClick={handleAiSuggestions} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'AI Suggestions'}
          </button>
        </div>
        {error && (
          <div className="error-message" style={{ color: 'red', marginTop: '10px' }}>
            {error}
          </div>
        )}
        {aiResult && !error && (
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