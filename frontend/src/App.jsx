import React, { useState, useEffect } from "react";

import Questionnaire from "./components/Questionnaire";
import axios from "axios";
import "./App.css";
import QUESTIONS_JSON from "./questions.json";
import Navbar from "./components/Navbar"; 
import { Route, Routes, useNavigate, Link } from 'react-router-dom';
import ProductInfo from "./components/ProductInfo";
import ProductPage from "./components/productPage";
import CompareLaptops from "./components/CompareLaptops";
import Wishlist from "./components/Wishlist";
import AuthPage from "./components/AuthPage";
import HomePage from "./components/HomePage";


const API_BASE_URL = "http://127.0.0.1:5000";


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
  const [wishlist, setWishlist] = useState([]);

  const handleWishlistUpdate = (model, action) => {
    if (action === 'add') {
      // Find the full laptop object from the main 'laptops' list
      const laptopToAdd = laptops.find(l => l.model === model);
      if (laptopToAdd && !wishlist.some(l => l.model === model)) {
        setWishlist(prev => [...prev, laptopToAdd]);
      } else {
        // If not found, force a full fetch (fallback)
        fetchWishlist();
      }
    } else if (action === 'remove') {
      setWishlist(prev => prev.filter(l => l.model !== model));
    }
  };

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

   const fetchWishlist = async () => {
    const currentToken = localStorage.getItem('token');
    // Only proceed if the user is authenticated
    if (!currentToken || !user) {
        setWishlist([]);
        return;
    }

    try {
        console.log("Fetching wishlist for user:", user.username);
        const res = await axios.get(`${API_BASE_URL}/wishlist`, {
            headers: {
                // Critical: Authorization header for protected route
                Authorization: `Bearer ${currentToken}`,
            },
        });
        // Assuming the backend returns the list of laptop objects
        setWishlist(res.data); 
    } catch (error) {
        console.error("Error fetching wishlist:", error);
        // If fetching fails, especially 401, clear the list
        setWishlist([]); 
        // We do not call handleLogout here, as the token check is done on the token state change.
    }
  };
  
  useEffect(() => {
    fetchWishlist();
  // DEPENDENCY FIX: Now runs whenever 'user' changes (login/logout)
  }, [user]); 

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
          <Route path="/" element={<HomePage />} />

          <Route path="/auth" element={<AuthPage user={user} onAuthSuccess={handleAuthSuccess} />} />
          
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
                      wishlist={wishlist}
                      onWishlistUpdate={handleWishlistUpdate}
                  />
              )
            ) : (
              <div id="not-signed-in">
                <h2 id='heading-not-signed-in'>Just a secccc.... <br />You haven't logged in yet
                </h2>
              
                <Link id='not-signed-in-link' to={'/auth'}>
                    <button className='not-signed-in-btn'>
                        Log In
                    </button>
                </Link>
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

        <Route path="/wishlist" element={
          <Wishlist user={user} wishlist = {wishlist} onWishlistUpdate={handleWishlistUpdate}/>
        }/>

        </Routes>  
      </div>
    </div>
  );
}

export default App;
