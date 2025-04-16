// App.js

import React, { useState } from 'react';
import './App.css';
// Replace these with your actual asset files (for example, locked.svg and unlocked.svg)
// import lockedIcon from './locked.svg';
// import unlockedIcon from './unlocked.svg';

import lockedIcon from './logo.svg';
import unlockedIcon from './logo.svg';

function App() {
  // Whether the dashboard is unlocked (after the entrance animation)
  const [isUnlocked, setIsUnlocked] = useState(false);
  // To control entrance animation (if you want to separate the animation state)
  const [isAnimating, setIsAnimating] = useState(false);
  // For controlling overlay modal display and its contents
  const [showOverlay, setShowOverlay] = useState(false);
  const [overlayContent, setOverlayContent] = useState(null);

  // Storage for our notes, tasks, and habits
  const [items, setItems] = useState({
    notes: [],
    tasks: [],
    habits: []
  });

  // Handles the entrance click: triggers an animation and then unlocks the dashboard.
  const handleLockClick = () => {
    setIsAnimating(true);
    // Simulate animation duration (e.g., 1 second)
    setTimeout(() => {
      setIsUnlocked(true);
      setIsAnimating(false);
    }, 1000);
  };

  // Opens the overlay modal to add a new item based on type.
  const openFormOverlay = (type) => {
    setOverlayContent({ type, mode: 'new' });
    setShowOverlay(true);
  };

  // Opens the overlay modal to display details about an existing item.
  const openDetailOverlay = (type, item) => {
    setOverlayContent({ type, item, mode: 'detail' });
    setShowOverlay(true);
  };

  // Closes the overlay modal.
  const closeOverlay = () => {
    setShowOverlay(false);
    setOverlayContent(null);
  };

  // Handles form submissions for new note/task/habit.
  const handleFormSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const type = formData.get('type');
    let newItem = {};

    if (type === 'note') {
      newItem = {
        id: Date.now(),
        content: formData.get('content')
      };
    } else if (type === 'task') {
      newItem = {
        id: Date.now(),
        title: formData.get('title'),
        dueDate: formData.get('dueDate')
      };
    } else if (type === 'habit') {
      newItem = {
        id: Date.now(),
        name: formData.get('name'),
        frequency: formData.get('frequency')
      };
    }

    setItems((prev) => ({
      ...prev,
      [type + 's']: [...prev[type + 's'], newItem]
    }));
    closeOverlay();
  };

  return (
    <div className="App">
      {/* Entrance Screen */}
      {!isUnlocked ? (
        <div
          className={`entrance ${isAnimating ? 'animate' : ''}`}
          onClick={handleLockClick}
        >
          {/* Show locked icon initially, then unlocked icon after animation */}
          <img
            src={isUnlocked ? unlockedIcon : lockedIcon}
            className="lock-icon"
            alt={isUnlocked ? 'Unlocked' : 'Locked'}
          />
          <p>Click the lock to unlock “Locked In”</p>
        </div>
      ) : (
        /* Main Dashboard */
        <div className="dashboard">
          <header className="dashboard-header">
            <h1>Locked In</h1>
            <div className="add-buttons">
            {/* buttons to overlay */}
              <button onClick={() => openFormOverlay('note')}>Add Note</button>
              <button onClick={() => openFormOverlay('task')}>Add Task</button>
              <button onClick={() => openFormOverlay('habit')}>Add Habit</button>
            </div>
          </header>

          <div className="dashboard-content">
            <section className="notes-section">
              <h2>Notes</h2>
              {items.notes.length === 0 && <p>No notes yet.</p>}
              {items.notes.map((note) => (
                <div
                  key={note.id}
                  className="note-item item"
                  onClick={() => openDetailOverlay('note', note)}
                >
                  {note.content}
                </div>
              ))}
            </section>

            <section className="tasks-section">
              <h2>Tasks</h2>
              {items.tasks.length === 0 && <p>No tasks yet.</p>}
              {items.tasks.map((task) => (
                <div
                  key={task.id}
                  className="task-item item"
                  onClick={() => openDetailOverlay('task', task)}
                >
                  <strong>{task.title}</strong> (Due: {task.dueDate})
                </div>
              ))}
            </section>

            <section className="habits-section">
              <h2>Habits</h2>
              {items.habits.length === 0 && <p>No habits yet.</p>}
              {items.habits.map((habit) => (
                <div
                  key={habit.id}
                  className="habit-item item"
                  onClick={() => openDetailOverlay('habit', habit)}
                >
                  <strong>{habit.name}</strong> (Frequency: {habit.frequency})
                </div>
              ))}
            </section>
          </div>
        </div>
      )}

      {/* Overlay Modal */}
      {showOverlay && (
        <div className="overlay">
          <div className="overlay-content">
            <button className="close-button" onClick={closeOverlay}>
              X
            </button>
            {overlayContent.mode === 'new' ? (
              // Form for new note/task/habit
              <form onSubmit={handleFormSubmit}>
                <input type="hidden" name="type" value={overlayContent.type} />
                {overlayContent.type === 'note' && (
                  <textarea
                    name="content"
                    placeholder="Enter note"
                    required
                  ></textarea>
                )}
                {overlayContent.type === 'task' && (
                  <>
                    <input
                      type="text"
                      name="title"
                      placeholder="Task Title"
                      required
                    />
                    <input type="date" name="dueDate" required />
                  </>
                )}
                {overlayContent.type === 'habit' && (
                  <>
                    <input
                      type="text"
                      name="name"
                      placeholder="Habit Name"
                      required
                    />
                    <select name="frequency" required>
                      <option value="">Select Frequency</option>
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                    </select>
                  </>
                )}
                <button type="submit">Save {overlayContent.type}</button>
              </form>
            ) : (
              // Detail/Editing overlay for an existing item with placeholder AI buttons
              <div className="overlay-detail">
                {overlayContent.type === 'note' && (
                  <>
                    <h3>Note Detail</h3>
                    <p>{overlayContent.item.content}</p>
                  </>
                )}
                {overlayContent.type === 'task' && (
                  <>
                    <h3>Task Detail</h3>
                    <p>
                      <strong>{overlayContent.item.title}</strong>
                    </p>
                    <p>Due Date: {overlayContent.item.dueDate}</p>
                  </>
                )}
                {overlayContent.type === 'habit' && (
                  <>
                    <h3>Habit Detail</h3>
                    <p>
                      <strong>{overlayContent.item.name}</strong>
                    </p>
                    <p>Frequency: {overlayContent.item.frequency}</p>
                  </>
                )}
                {/* Placeholder buttons for potential future AI functionality */}
                <div className="future-actions">
                  <button>AI Edit</button>
                  <button>AI Suggestions</button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
