// src/App.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import DashboardPage from './pages/DashboardPage';
import Layout from './components/Layout';
// --- Import ProtectedRoute ---
import ProtectedRoute from './components/ProtectedRoute';
// --------------------------

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* --- Apply ProtectedRoute --- */}
        <Route element={<ProtectedRoute />}>
          {/* Routes nested inside ProtectedRoute require authentication */}
          <Route path="/dashboard" element={<DashboardPage />} />
          {/* Add other protected routes here later (e.g., chatbot details) */}
        </Route>
        {/* --------------------------- */}

        <Route path="*" element={<h2>Page Not Found</h2>} />
      </Routes>
    </Layout>
  );
}

export default App;