import React from 'react'
import './navbar.css'

export default function navbar() {
  return (
    <div>
        <div className="navbar">
            <h1 id='brand'>Smart Select: Tech Chosen Right</h1>
            <div className="comps-nav">
              <div className="register-nav">
                Login/Signup
              </div>
              <div className="Redo-nav">
                Redo
              </div>
              <div className="wishlist-nav">
                <i class="fa-solid fa-heart"></i>
              </div>
            </div>
        </div>

    </div>
  )
}
