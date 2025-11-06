import React, { useState, useEffect, useRef } from 'react'
import { useParams, Link, useLocation } from 'react-router-dom';
import './navbar.css'

export default function Navbar({user, onLogOut}) {

  const menuRef = useRef(null);

  const location = useLocation();

  // State to manage the visibility of the dropdown menu
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Function to toggle the menu open/closed
  const toggleMenu = () => {
    setIsMenuOpen(prev => !prev);
  };

  // useEffect to handle outside clicks
  useEffect(() => {
    /**
     * Closes the menu if the click is outside the referenced component
     */
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsMenuOpen(false);
      }
    }
    
    // Bind the event listener
    document.addEventListener("mousedown", handleClickOutside);
    
    // Unbind the event listener on cleanup
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [menuRef]); // Dependency array ensures the effect runs only once

  return (
    <div>
        <div className="navbar">
          <div id='brand'>
            <Link id="nav-link" to="/">
              <h1>Smart Select: Tech Chosen Right</h1>
            </Link>
          </div>
            <div className="comps-nav">
                {user ? 
                (
                  <>
                    <div className="register-nav" onClick={toggleMenu}>
                      Hello, {user.username}!
                    </div>
                    {/* <div className="register-nav" onClick={onLogOut} style={{cursor: 'pointer'}}>
                      Logout
                    </div> */}
                    {/* <Link id="nav-link" to="/questionnaire">
                    <div className="Redo-nav">
                      Redo
                    </div>
                    </Link> */}
                      <Link to="/wishlist" id="nav-link">
                      <div className="wishlist-nav">
                        <i class="fa-solid fa-heart"></i>
                      </div>
                    </Link>

                    {/* 3. The Dropdown/Popup menu, conditionally rendered */}
                    {isMenuOpen && (
                      <div className="user-dropdown-menu" ref={menuRef}>
                          <Link to="/questionnaire" className="menu-item, nav-link, menu-item" onClick={toggleMenu}>
                              Go to Quiz
                          </Link>
                          <Link to="/wishlist" className="menu-item, nav-link, menu-item" onClick={toggleMenu}>
                              Wish List
                          </Link>
                          <div className="menu-item, logout-item " onClick={() => {
                              onLogOut();
                              toggleMenu(); // Close the menu after logging out
                          }}>
                              Logout
                          </div>
                      </div>
                    )}
                  </>
                ):  location.pathname === "/auth" ? (
                  <div className="register-nav not-logged-in">
                    Helloo!
                  </div>
                ) : (
                  <Link id="nav-link" className="not-logged-in" to="/auth">
                    <div className="register-nav">Login</div>
                  </Link>
                )}
              </div>
            </div>
        </div>
  )
}
