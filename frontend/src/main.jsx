/**
 * ==============================================================================
 * PRE-AI Frontend Entry Point (src/main.jsx)
 * ------------------------------------------------------------------------------
 * Mounts the React root application and loads the modern developer design system.
 * ==============================================================================
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
