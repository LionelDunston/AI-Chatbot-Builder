// src/components/Layout.jsx
import React from 'react';
import { Link } from 'react-router-dom'; // Import Link for navigation

// Basic inline styles (replace with CSS later)
const headerStyle = {
    backgroundColor: '#f0f0f0',
    padding: '10px 20px',
    marginBottom: '20px',
    borderBottom: '1px solid #ccc'
};

const navStyle = {
    display: 'flex',
    gap: '15px'
};

const mainStyle = {
    padding: '0 20px'
};

// The Layout component accepts 'children' which will be the page content
function Layout({ children }) {
  return (
    <div>
      <header style={headerStyle}>
        <nav style={navStyle}>
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          {/* Add Login/Logout links later based on auth state */}
          <Link to="/login">Login</Link>
        </nav>
      </header>
      <main style={mainStyle}>
        {children} {/* Renders the active page component here */}
      </main>
      {/* You could add a footer here */}
    </div>
  );
}

export default Layout;