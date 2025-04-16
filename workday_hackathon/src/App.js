// App.js

import React, { useState } from 'react';
import './App.css';
import './Overlay.css'; // Include overlay-specific CSS

// For demo purposes we reuse logo.svg as both lock icons.
import lockedIcon from './logo.svg';
import unlockedIcon from './logo.svg';

import OverlayForm from './components/OverlayForm';
import OverlayDetail from './components/OverlayDetail';


function App() {
  // Whether the dashboard is unlocked (after the entrance animation)
  const [isUnlocked, setIsUnlocked] = useState(false);
  // To control entrance animation (if you want to separate the animation state)
  const [isAnimating, setIsAnimating] = useState(false);
  // Overlay state: if an overlay should be shown and its content details.
  const [overlayData, setOverlayData] = useState({
    show: false,
    mode: null, // either 'new' or 'detail'
    type: null, // 'note', 'task', or 'habit'
    item: null, // only used in detail mode
  });

  // Storage for our notes, tasks, and habits.
  const [items, setItems] = useState({
    notes: [],
    tasks: [],
    habits: [],
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
    setOverlayData({
      show: true,
      mode: 'new',
      type,
      item: null,
    });
  };

  // Opens the overlay modal to display details about an existing item.
  const openDetailOverlay = (type, item) => {
    setOverlayData({
      show: true,
      mode: 'detail',
      type,
      item,
    });
  };

  // Closes any overlay modal.
  const closeOverlay = () => {
    setOverlayData({
      show: false,
      mode: null,
      type: null,
      item: null,
    });
  };

  // Handles form submissions for new note/task/habit.
  const handleFormSubmit = (data) => {
    // data is an object containing the fields from our overlay form.
    const type = data.type;
    let newItem = { id: Date.now(), ...data };
    // Remove any extraneous key if needed
    delete newItem.type;

    setItems((prev) => ({
      ...prev,
      [type + 's']: [...prev[type + 's'], newItem],
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
          <img
            src={isUnlocked ? unlockedIcon : lockedIcon}
            className="lock-icon"
            alt={isUnlocked ? 'Unlocked' : 'Locked'}
          />
          <p>Click the lock to unlock “Locked In”</p>
        </div>
      ) : (
        // Main Dashboard
        <div className="dashboard">
          <header className="dashboard-header">
            <h1>Locked In</h1>
            <div className="add-buttons">
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
      {overlayData.show &&
        (overlayData.mode === 'new' ? (
          <OverlayForm
            type={overlayData.type}
            onClose={closeOverlay}
            onSubmit={handleFormSubmit}
          />
        ) : (
          <OverlayDetail
            type={overlayData.type}
            item={overlayData.item}
            onClose={closeOverlay}
          />
        ))}
    </div>
  );
}

export default App;
