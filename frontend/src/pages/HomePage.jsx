// src/pages/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom'; // For navigation links

function HomePage() {
  return (
    <div>
      <h2>Home Page</h2>
      <nav>
        <ul>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/signup">Sign Up</Link></li>
          <li><Link to="/dashboard">Dashboard (Protected)</Link></li>
        </ul>
      </nav>
    </div>
  );
}

export default HomePage;