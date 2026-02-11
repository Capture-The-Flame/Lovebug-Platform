import React, { useState } from 'react';
import './LovebugLogin.css';


const LovebugLogin = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!username.trim()) {
      setError('Please enter a username');
      return;
    }

    setLoading(true);
    setError('');

    try {
      localStorage.setItem('ctf_username', username.trim());
      onLoginSuccess({ authenticated: true, username: username.trim() });
    } catch (err) {
      console.error('Login error:', err);
      setError('Failed to log in');
    } finally {
      setLoading(false);
    }
  };

  const BinaryHeart = () => {
    const heartLines = [
      '***********                  ***********',
      '*****************            *****************',
      '*********************        *********************',
      '***********************      ***********************',
      '************************    ************************',
      '*************************  *************************',
      '**************************************************',
      '************************************************',
      '********************************************',
      '****************************************',
      '**********************************',
      '******************************',
      '************************',
      '********************',
      '**************',
      '**********',
      '******',
      '**',
    ];

    return (
      <div className="binary-heart">
        {heartLines.map((line, index) => (
          <div key={index} className="heart-line" style={{ '--line-index': index }}>
            {line}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="lovebug-login">
      <div className="lovebug-container">
        <BinaryHeart />
        <div className="menu-section">
          <h1 className="title">Caught the Lovebug</h1>
          <form onSubmit={handleLogin} className="menu-options">
            <input
              type="text"
              className="username-input"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={loading}
              autoFocus
            />
            {error && <div className="error-message">{error}</div>}
            <button 
              type="submit" 
              className="menu-item" 
              disabled={loading}
            >
              {loading ? 'Logging in...' : 'Enter CTF'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LovebugLogin;