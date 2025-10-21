import React, { useState, useEffect } from "react";

import Questionnaire from "./components/Questionnaire";
import axios from "axios";
import "./App.css";
import QUESTIONS_JSON from "./questions.json";
import Navbar from "./components/Navbar"; 
import { Route, Routes, useNavigate } from 'react-router-dom';
import ProductInfo from "./components/ProductInfo";
import ProductPage from "./components/productPage";
import CompareLaptops from "./components/CompareLaptops";
import Login from "./components/Login";
import SignUp from "./components/SignUp";



function App() {
  const navigate = useNavigate();

  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null); // Optional: Store user info

  const [results, setResults] = useState(() => {
    // Load from localStorage if available
    const saved = localStorage.getItem("results");
    return saved ? JSON.parse(saved) : null;
  });

  const [query, setQuery] = useState("");
  const [laptops, setLaptops] = useState([]);

  // Whenever results change, save to localStorage
  useEffect(() => {
    if (results) {
      localStorage.setItem("results", JSON.stringify(results));
    } else {
      localStorage.removeItem("results");
    }
  }, [results]);

  useEffect(() => {
    // Fetch laptops from backend when results are available
    if (results && !results.processing) {
      axios
        .get("http://127.0.0.1:5000/laptops")
        .then((res) => setLaptops(res.data))
        .catch((err) => console.error(err));
    }
  }, [results]);

  // 2. NEW: Function to decode token (simplistic) and set user info
  const decodeToken = (jwtToken) => {
    try {
      // Note: This is a basic client-side decode. 
      // It doesn't verify the signature, only reads the payload.
      const payload = JSON.parse(atob(jwtToken.split('.')[1]));
      setUser({ username: payload.username, id: payload.user_id });
    } catch (e) {
      console.error("Failed to decode token:", e);
      setUser(null);
      setToken(null);
      localStorage.removeItem("token");
    }
  };

  // 3. NEW: Effect to initialize user from token
  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      decodeToken(token);
    } else {
      localStorage.removeItem("token");
      setUser(null);
    }
  }, [token]);

  // 4. NEW: Handle Logout
  const handleLogout = () => {
    setToken(null);
    navigate('/');
  };

  // 5. NEW: Handle successful Login/Signup
  const handleAuthSuccess = (token) => {
    setToken(token);
    navigate('/questionnaire'); // Redirect after successful auth
  };

  const handleSubmit = async (answers) => {
    setResults({ processing: true });
    navigate('/recommendations');
    const res = await axios.post("http://127.0.0.1:5000/query", { answers });
    setResults(res.data);
    setQuery("");
  };

  const handleUpdateQuery = async () => {
    if (!query) return;
    setResults({ processing: true });
    // The backend should handle combining the original answers with the custom_query
    const res = await axios.post("http://127.0.0.1:5000/query", {
      custom_query: query,
    });
    setResults(res.data);
    setQuery("");
  };

  const handleReset = () => {
    setResults(null);
    localStorage.removeItem("results");
  };

  return (
    <div className="App-container">
      <Navbar user={user} onLogOut={handleLogout} />
      <div className="main-content">
        <Routes>
          <Route path="/" element={
            <div className="home-page">
              <h2>Welcome to Smart Select: Tech Chosen Right</h2>
              Get Started     
              <p>Your journey to finding the perfect laptop starts here.</p>
              <button onClick={() => window.location.href = "/recommendations"}>
                Get Started
              </button>
              {/* <button onClick={() => window.location.href = "/login"}>
                Login
              </button>
              <button onClick={() => window.location.href = "/signup"}>
                SignUp
              </button> */}
            </div>
          } />  
          <Route path="/login" element={
            <Login user={user} onAuthSuccess={handleAuthSuccess}/>
          }/>

          <Route path="/signup" element={
            <SignUp user={user} onAuthSuccess={handleAuthSuccess}/>
          }/>
            
          
          <Route path="/questionnaire" element={
            <Questionnaire user={user} questions={QUESTIONS_JSON.questions} onSubmit={handleSubmit} />
          } />

          <Route path="/recommendations" element={
          <>
            {results ? ( 
              results.processing ? (
                <div className="loading">
                  <div className="loader"></div>
                </div>
              ) : (
                  <ProductPage user={user} 
                      laptops={laptops}
                      query={query}
                      setQuery={setQuery}
                      onUpdateQuery={handleUpdateQuery}
                      onReset={handleReset}
                  />
              )
            ) : (
              // User landed here without submitting, redirect them to the questionnaire
              <div className="no-results-message">
                  No recommendations found. Please <a href="/questionnaire">complete the questionnaire</a>.
              </div>
            )}
          </>
        } />
        <Route path="/products/:id" element={
          <ProductInfo user={user} laptops={laptops} />
        } />

        <Route path="/compareLaptops" element={
          <CompareLaptops user={user} laptops={laptops}/>
        }/>

        </Routes>  
      </div>
    </div>
  );
}

export default App;
