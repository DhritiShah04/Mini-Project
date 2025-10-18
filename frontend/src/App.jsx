import React, { useState, useEffect } from "react";

import Questionnaire from "./components/Questionnaire";
import axios from "axios";
import "./App.css";
import QUESTIONS_JSON from "./questions.json";
import Navbar from "./components/Navbar"; 
import { Route, Routes, useNavigate } from 'react-router-dom';
import ProductInfo from "./components/ProductInfo";
import ProductCards from "./components/productPage";
import CompareLaptops from "./components/CompareLaptops";


function App() {
  const navigate = useNavigate();

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
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={
            <div className="home-page">
              <h2>Welcome to Smart Select: Tech Chosen Right</h2>
              <p>Your journey to finding the perfect laptop starts here.</p>
              <button onClick={() => window.location.href = "/questionnaire"}>
                Get Started
              </button>
            </div>
          } />  
          <Route path="/questionnaire" element={
            <Questionnaire questions={QUESTIONS_JSON.questions} onSubmit={handleSubmit} />
          } />

          <Route path="/recommendations" element={
          <>
            {results ? ( 
              results.processing ? (
                  <div className="loading">Loading recommendations...</div>
              ) : (
                  <ProductCards
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
          <ProductInfo laptops={laptops} />
        } />

        <Route path="/compareLaptops" element={
          <CompareLaptops laptops={laptops}/>
        }/>

        </Routes>

        
      </div>
    </div>
  );
}

export default App;
