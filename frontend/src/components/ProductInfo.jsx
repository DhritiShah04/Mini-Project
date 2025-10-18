import React from 'react';
import { useParams } from 'react-router-dom';
// import './ProductInfo.css';

// Define the keys that might be considered "More Info" (excluding the ones already shown in the card body if desired)
const DETAIL_KEYS = [
    "model",
    "cpu",
    "ram",
    "storage",
    "gpu",
    "display",
    "battery",
    "price_inr",
    "why",
];

function ProductInfo({ laptops }) {

  const { id } = useParams();

  // / 🚨 CRITICAL FIX: Ensure both sides are strings for comparison.
  // We assume the ObjectId object is stored under the key '_id'.
  const item = laptops.find(laptop => {
      // 1. Check if the _id field exists.
      if (laptop._id) {
          // 2. Convert the ObjectId object to its string representation 
          //    (e.g., using .toString() or .toHexString()) and compare it to the URL ID.
          //    We use String() for maximum safety.
          return String(laptop._id) === id;
      }
      return false;
  });

  if (!item) {
    return (
        <div className="product-info-details">
            <h2>Error: Product details not found for ID: {id}</h2>
        </div>
    );
  }

  return (
    <div className="product-info-details">
      <h1>{item.model}</h1> {/* Display model name as the title */}
      <h3>Full Specifications</h3>
      
      {DETAIL_KEYS.map((key) => (
        <div key={key} className="spec-item">
          <strong className="spec-label">{key.replace('_inr', ' (INR)').toUpperCase()}:</strong>
          <span className="spec-value">{item[key] || "N/A"}</span>
        </div>
      ))}
      
      <p className="why-text">
        **Recommendation Rationale:** {item.why || "Rationale unavailable."}
      </p>

    </div>

    
  );
}

export default ProductInfo;
