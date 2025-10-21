import React, { useRef, useEffect } from 'react';
import './productPage.css' 
import ProductCard from './productCard';
import { Link } from 'react-router-dom';

// The MyPage component is empty and can be removed or ignored for this functionality.
// const MyPage = () => {
//   // ... (Scrolling logic was incorrectly placed here)
// }


// Accept laptops data, plus state and handlers for the query bar
function ProductCards({user, laptops, query, setQuery, onUpdateQuery, onReset }) {
  // 1. ✅ CORRECT LOCATION: Declare the ref inside the component that uses it
  const targetDivRef = useRef(null);

  // 2. ✅ CORRECT LOCATION: Define the scroll logic here
  useEffect(() => {
    // Check if the ref has been attached to the element
    if (targetDivRef.current) {
      // Use scrollIntoView with block: 'center' to center it vertically
      targetDivRef.current.scrollIntoView({
        behavior: 'smooth', // Optional: 'instant' or 'smooth'
        block: 'center',    // Centers it vertically in the viewport
        inline: 'nearest'   // Minimizes horizontal scrolling
      });
    }
    // The dependency array is empty so it runs only once after the component mounts
  }, []);


  if (!laptops || laptops.length === 0) {
    return (
      // ... (No laptops found JSX)
      <div className='product-cards-container'>
        <div id="topbar" className="query-section">
          <p>No laptops found based on current criteria. Try refining your search:</p>
          <input id='refine-input-topbar'
            type="text"
            placeholder="Type something like 'increase budget' or 'gaming laptop'"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={onUpdateQuery}>
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
          <button className="reset-btn" onClick={onReset}>Start Over</button>
        </div>
      </div>
    );
  }

  return (
    <>
      {user ? (
        <div className='product-cards-container'>
          {/* Refinement Bar at the top */}
          <div id="topbar" className="query-section">
            <input id='topbar-ip'
              type="text"
              placeholder="Refine your query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button id='search' onClick={onUpdateQuery}>
              <i  class="fa-solid fa-magnifying-glass"></i>
            </button> 
          </div>

          {/* 3. ✅ USAGE: The ref is attached here and now works! */}
          <div ref={targetDivRef} class="main-cont">
            <div id="prod">
              {laptops.map((item, idx) => (
                <ProductCard user={user} 
                  key={item._id || idx} 
                  item={item}
                />
              ))}
            </div>
            <div id="go-to-compare">
              <Link to="/compareLaptops"> 
                <button>
                  Compare
                </button>
              </Link>
            </div>
          </div>
        </div>
      ):(
        <div id="not-signed-in">
          <h2 id='heading-not-signed-in'>Just a secccc.... <br />You haven't logged in yet
          </h2>
        
          <Link id='not-signed-in-link' to={'/login'}>
              <button className='not-signed-in-btn'>
                  Log In
              </button>
          </Link>
        </div>
      )}
    </>
  )
}

export default ProductCards;