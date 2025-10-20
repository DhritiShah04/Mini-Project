import React from 'react'
import './productCard.css'
import { Link } from 'react-router-dom';

// Define the keys we want to display and format them
const DISPLAY_KEYS = [
    "_id",
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

function ProductCard({ item }) {
  const productId = item._id ? item._id.toString() : item.id; // Use item.id as fallback
  return (
      <div className="recommendation-card">
        <div id="prod-img">

        </div>
        <div id="prod-deets">
          <div className="prod-model-comp">
            <h3 className="product-model">{item.model || "Unknown Model"} <br /> ₨ {item.price_inr}/-
            </h3>
          </div>
          {/* <h4 className='prod-price'>₨ {item.price_inr}/-</h4> */}
          <div className="prod-why-comp">
            <p id="prod-why">{item.why}</p>
          </div>
        </div>

        <div className="more-info">
          <Link id='more-info-link' to={`/products/${productId}`}> 
            <button id='info'>
              More Info
            </button>
          </Link>
          <button id='wish'>
            <i id='heart' class="fa-solid fa-heart"></i>
          </button>
        </div>
          {/* {DISPLAY_KEYS.map((key) => (
              <div key={key}>
                  <strong>{key.replace('_inr', '').toUpperCase()}:</strong> {item[key] || "Unknown"}
          
            
                  </div>
          ))} */}
      </div>
  )
}

export default ProductCard
