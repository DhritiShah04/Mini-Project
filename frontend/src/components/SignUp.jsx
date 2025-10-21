import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './login_signup.css'

const API_BASE_URL = "http://127.0.0.1:5000";

function Signup({user}) {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/signup`, {
        username,
        password,
      });

      setMessage(response.data.message || 'Signup successful! Please log in.');
      
      // Redirect to questionnaire page after successful signup
      setTimeout(() => navigate('/questionnaire'), 1500); 

    } catch (err) {
      const msg = err.response?.data?.message || 'Signup failed. Please try a different username.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="body">
      {user ? (
        <>
          <h2 className='heading-reg'>{user.username}, you have already signed in</h2>
          
          <Link className='link-reg' to={'/recommendations'}>
              <button className='alr-reg-btn'>
                  Go to Recommendations
              </button>
          </Link>
      </>
      ) : (
        <>
          <div className="main-cont-reg">
            <h2 className='heading-reg'>Sign Up</h2>
            <form onSubmit={handleSubmit} className="form-reg">
              {error && <p className="auth-error">{error}</p>}
              {message && <p className="auth-success">{message}</p>}
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
                {loading ? 'Signing up...' : 'Sign Up'}
              </button>
            </form>
            <p className="switch-reg">
              Already have an account? <Link to="/login">Login</Link>
            </p>
          </div>
        </>
      )}
    </div>
  );
}

export default Signup;