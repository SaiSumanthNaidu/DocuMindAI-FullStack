import { NavLink } from "react-router-dom";

import "./Navbar.css";

function Navbar() {
  return (
    <header className="navbar">

      <div className="container navbar-container">

        <NavLink to="/" className="logo">

            <span className="logo-text">
                DocuMind AI
            </span>

        </NavLink>

        <nav className="nav-links">

            <NavLink to="/">Home</NavLink>

            <NavLink to="/about">About</NavLink>

            <div className="auth-buttons">

                <NavLink to="/login" className="login-link">
                    Login
                </NavLink>

                <NavLink to="/register" className="register-btn">
                    Register
                </NavLink>

            </div>

        </nav>

      </div>

    </header>
  );
}

export default Navbar;