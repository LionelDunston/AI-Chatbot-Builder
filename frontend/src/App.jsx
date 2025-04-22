// src/App.jsx
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom'; // Import routing components

// Import page components
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import DashboardPage from './pages/DashboardPage';
// Import a basic Layout component (we'll create this next)
import Layout from './components/Layout';

function App() {
  return (
    // Use the Layout component to wrap all routes
    <Layout>
      <Routes> {/* Define all possible routes */}
        <Route path="/" element={<HomePage />} /> {/* Route for the homepage */}
        <Route path="/login" element={<LoginPage />} /> {/* Route for the login page */}
        <Route path="/signup" element={<SignupPage />} /> {/* Route for the signup page */}
        {/* We'll add protection to this route later */}
        <Route path="/dashboard" element={<DashboardPage />} /> {/* Route for the dashboard */}

        {/* Optional: Add a catch-all route for 404 Not Found */}
        <Route path="*" element={<h2>Page Not Found</h2>} />
      </Routes>
    </Layout>
  );
}

export default App;