import React, { useState } from 'react';
import './Login.css';

// Get credentials from environment variables
const CORRECT_USERNAME = process.env.REACT_APP_LOGIN_USERNAME || '';
const CORRECT_PASSWORD = process.env.REACT_APP_LOGIN_PASSWORD || '';

// Debug: Log environment variables (remove in production)
console.log('Environment variables check:', {
  REACT_APP_LOGIN_USERNAME: process.env.REACT_APP_LOGIN_USERNAME ? 'SET' : 'NOT SET',
  REACT_APP_LOGIN_PASSWORD: process.env.REACT_APP_LOGIN_PASSWORD ? 'SET' : 'NOT SET',
  allEnvKeys: Object.keys(process.env).filter(key => key.startsWith('REACT_APP_'))
});

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validate that credentials are configured
    if (!CORRECT_USERNAME || !CORRECT_PASSWORD) {
      setError('Login credentials not configured. Please check environment variables.');
      setLoading(false);
      return;
    }

    // Simulate a small delay for better UX
    setTimeout(() => {
      if (username === CORRECT_USERNAME && password === CORRECT_PASSWORD) {
        // Store authentication in localStorage
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('username', username);
        onLogin();
      } else {
        setError('Invalid username or password');
        setLoading(false);
      }
    }, 300);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>ASC Survey Dashboard</h1>
        <h2>Sign In</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
              autoFocus
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="login-button" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;

