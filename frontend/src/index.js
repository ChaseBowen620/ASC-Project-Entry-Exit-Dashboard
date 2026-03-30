import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Full page load / browser refresh: start at the top (don't restore prior scroll).
if ('scrollRestoration' in window.history) {
  window.history.scrollRestoration = 'manual';
}
window.scrollTo(0, 0);
window.addEventListener(
  'load',
  () => {
    window.scrollTo(0, 0);
  },
  { once: true }
);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

