import React from 'react'
import { useParams, Link } from 'react-router-dom';
import './navbar.css'

export default function navbar({user, onLogOut}) {
  return (
    <div>
        <div className="navbar">
            <h1 id='brand'>Smart Select: Tech Chosen Right</h1>
            <div className="comps-nav">
                {user ? 
                (
                  <>
                    <div className="register-nav">
                      Hello, {user.username}!
                    </div>
                    <div className="register-nav" onClick={onLogOut} style={{cursor: 'pointer'}}>
                      Logout
                    </div>
                    <Link id="nav-link" to="/questionnaire">
                    <div className="Redo-nav">
                      Redo
                    </div>
                    </Link>
                    <div className="wishlist-nav">
                      <i class="fa-solid fa-heart"></i>
                    </div>
                  </>
                ): (
                  <Link id="nav-link" className='not-logged-in' to="/login">
                  <div className="register-nav">
                    {/* Home */}
                  </div>
                </Link>
                )}
              </div>
            </div>
        </div>
  )
}
