// src/components/Layout.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Corrected import path assumed

// Define styles at the top level of the file
const headerStyle = {
    backgroundColor: '#f0f0f0',
    padding: '10px 20px',
    marginBottom: '20px',
    borderBottom: '1px solid #ccc'
};

const navStyle = {
    display: 'flex',
    gap: '15px',
    alignItems: 'center' // Align items vertically in the nav
};

const mainStyle = {
    padding: '0 20px'
};

const userEmailStyle = {
    marginRight: '15px', // Add some space before the logout button
    fontStyle: 'italic'
};

const logoutButtonStyle = {
    background: 'none',
    border: 'none',
    color: '#007bff',
    cursor: 'pointer',
    padding: 0,
    textDecoration: 'underline',
    fontSize: 'inherit' // Match surrounding text size
};


function Layout({ children }) {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div>
      <header style={headerStyle}>
        <nav style={navStyle}>
          <Link to="/">Home</Link>
          {isAuthenticated && <Link to="/dashboard">Dashboard</Link>}

          {isAuthenticated ? (
             <>
                {/* Optional: Add some space */}
                <span style={{ flexGrow: 1 }}></span> {/* Pushes login/logout to the right */}
                {user && <span style={userEmailStyle}>Welcome, {user.email}!</span>}
                <button onClick={handleLogout} style={logoutButtonStyle}>
                  Logout
                </button>
             </>
          ) : (
             <>
               <span style={{ flexGrow: 1 }}></span> {/* Pushes login/logout to the right */}
               <Link to="/login">Login</Link>
               <Link to="/signup">Sign Up</Link> {/* Added Signup Link */}
             </>
          )}
        </nav>
      </header>
      <main style={mainStyle}>
        {children}
      </main>
    </div>
  );
}

export default Layout;