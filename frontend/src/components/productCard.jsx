import React, { useState, useEffect } from 'react'
import './productCard.css'
import { Link } from 'react-router-dom';
import axios from 'axios';

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

const API_BASE_URL = "http://127.0.0.1:5000";

function ProductCard({initialWishlist, user, item, onWishlistUpdate }) {
  const [isWishlisted, setIsWishlisted] = useState(initialWishlist || false)

  useEffect(() => {
    setIsWishlisted(initialWishlist || false);
  }, [initialWishlist]);

  const handleWishlistToggle = async () => {
    if(!user) {
      alert("Please log in before you can add items to your wishlist")
      return;
    }

    const action = isWishlisted ? "remove" : "add";
    const endpoint = `${API_BASE_URL}/wishlist/${action}`;

    try {
      const token = localStorage.getItem('token');
      console.log("Token sent:", token);

      const res = await axios.post(endpoint, {
        model: item.model
      },{
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if(res.status === 200 || res.status === 201)
      {
        if (onWishlistUpdate) {
          onWishlistUpdate(item.model, action);
        }
        setIsWishlisted(!isWishlisted)
      }
    }

    catch(error) {
      console.error("Wishlist operation failed:", error);
      alert("Failed to update wishlist. Please try again.");
    }
  }


  const productId = item._id ? item._id.toString() : item.id; // Use item.id as fallback
  return (
    <>
      {user ? (
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
            <button id='wish' onClick={handleWishlistToggle}>
              <i id='heart' class={`fa-solid fa-heart ${isWishlisted ? 'wishlisted': 'not wishlisted'}`} style={{color: isWishlisted ? '#D25D5D' : '#b9b7b7'}}></i>
            </button>
          </div>
            {/* {DISPLAY_KEYS.map((key) => (
                <div key={key}>
                    <strong>{key.replace('_inr', '').toUpperCase()}:</strong> {item[key] || "Unknown"}
            
              
                    </div>
            ))} */}
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

export default ProductCard
