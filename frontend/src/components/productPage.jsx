import React from 'react'
import './productPage.css' 
import ProductCard from './productCard';

// Accept laptops data, plus state and handlers for the query bar
function ProductCards({ laptops, query, setQuery, onUpdateQuery, onReset }) {


  if (!laptops || laptops.length === 0) {
    return (
      <div className='product-cards-container'>
        {/* Topbar when no laptops are found */}
        <div id="topbar" className="query-section">
          <p>No laptops found based on current criteria. Try refining your search:</p>
          <input
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
    <div className='product-cards-container'>
      {/* Refinement Bar at the top */}
      <div id="topbar" className="query-section">
        <input
          type="text"
          placeholder="Refine your query..."
          value={query} // Use the passed-down query state
          onChange={(e) => setQuery(e.target.value)} // Use the passed-down setQuery function
        />
        {/* Button to trigger the update */}
        <button onClick={onUpdateQuery}>
          <i class="fa-solid fa-magnifying-glass"></i> Refine
        </button> 
        {/* Button to trigger the reset */}
        <button className="reset-btn" onClick={onReset}>Start Over</button>
      </div>

      <div id="main-cont">
        <div id="prod">
          {laptops.map((item, idx) => (
            <ProductCard 
              key={item._id || idx} 
              item={item} // Pass the individual laptop item as a prop
            />
          ))}
        </div>
        <div id="go-to-compare">
          <button>
            Compare
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProductCards
