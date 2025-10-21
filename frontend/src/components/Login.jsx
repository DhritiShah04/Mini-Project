import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import './login_signup.css'

const API_BASE_URL = "http://127.0.0.1:5000";

function Login({ user, onAuthSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/login`, {
        username,
        password,
      });

      // 1. Get the JWT token from the backend response
      const token = response.data.token; 
      
      // 2. Call the handler from App.jsx to set state and localStorage
      onAuthSuccess(token); 

    } catch (err) {
      // Handle errors (e.g., 401 Unauthorized from the server)
      const message = err.response?.data?.message || 'Login failed. Please check your credentials.';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="body">
        {user ? (
            <>
                <h2 className='heading-reg'>{user.username}, you are already logged in</h2>
                
                <Link className='link-reg' to={'/recommendations'}>
                    <button className='alr-reg-btn'>
                        Go to Recommendations
                    </button>
                </Link>
            </>
        ):(
            <>
                <div className="main-cont-reg">
                    {/* <div className="auth-card"> */}
                    <h2 className='heading-reg'>Login</h2>
                    
                    
                    {/* <div className="form-reg"> */}
                    <form onSubmit={handleSubmit} className="form-reg">
                        {error && <p className="auth-error">{error}</p>}

                        <label htmlFor="username">Username</label>
                        <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        disabled={loading}
                        />

                        <label htmlFor="password">Password</label>
                        <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        disabled={loading}
                        />

                        <button type="submit" disabled={loading} className="auth-button">
                        {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </form>
                    {/* </div> */}

                    
                    <p className="switch-reg">
                    Don't have an account? <Link to="/signup">Sign Up</Link>
                    </p>
                </div>
            </>
        )}
        
    </div>
  );
}

export default Login;