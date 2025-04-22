// src/contexts/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import { loginUser as apiLogin, signupUser as apiSignup, getCurrentUser as apiGetCurrentUser } from '../services/api'; // Use alias for clarity

// Create the context
const AuthContext = createContext(null);

// Create the provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Stores user object if logged in
  const [token, setToken] = useState(localStorage.getItem('authToken')); // Load token from storage initially
  const [loading, setLoading] = useState(true); // Loading state for initial check

  // Effect to set Authorization header on apiClient when token changes
  useEffect(() => {
      // You might need to import apiClient directly here or manage this differently
      // For simplicity now, we handle header in api calls needing it
      // OR: Set default header on the imported instance (can have side effects)
      // if (token) {
      //     apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // } else {
      //     delete apiClient.defaults.headers.common['Authorization'];
      // }

      // Fetch user details if token exists but user data is missing
      const fetchUserOnLoad = async () => {
          if (token && !user) {
              try {
                  const response = await apiGetCurrentUser(token);
                  setUser(response.data);
              } catch (error) {
                  console.error("Failed to fetch user on load:", error);
                  // Token might be invalid/expired, clear it
                  logout();
              }
          }
          setLoading(false); // Finish loading check
      };

      fetchUserOnLoad();
  }, [token]); // Rerun when token changes

  const login = async (email, password) => {
    try {
      const response = await apiLogin(email, password);
      const { access_token } = response.data;
      localStorage.setItem('authToken', access_token); // Store token
      setToken(access_token); // Update state
      // Fetch user data after successful login
      const userResponse = await apiGetCurrentUser(access_token);
      setUser(userResponse.data); // Update user state
      return true; // Indicate success
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      logout(); // Clear any invalid state on failure
      throw error; // Re-throw error for component to handle
    }
  };

  const signup = async (email, password) => {
    try {
      const response = await apiSignup(email, password);
      // Optionally log the user in immediately after signup
      await login(email, password); // Attempt login after successful signup
      return true;
    } catch (error) {
      console.error("Signup failed:", error.response?.data || error.message);
       throw error; // Re-throw error for component to handle
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken'); // Remove token from storage
    setToken(null); // Clear token state
    setUser(null); // Clear user state
    // Remove default header if it was set
    // delete apiClient.defaults.headers.common['Authorization'];
  };

  // Value provided by the context
  const value = {
    user, // The logged-in user object (or null)
    token, // The auth token (or null)
    isAuthenticated: !!token, // Boolean flag for easy checks
    loading, // Indicate if initial auth check is loading
    login,
    signup,
    logout,
  };

  // Render children wrapped in the context provider
  // Only render children once loading is complete to avoid flashes of wrong content
  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Custom hook to easily use the auth context in components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};