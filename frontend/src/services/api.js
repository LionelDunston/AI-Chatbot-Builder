// src/services/api.js
import axios from 'axios';

// Define the base URL for your backend API
// Make sure this matches where your backend is running
// If frontend and backend run on different ports locally during dev,
// you might need to configure CORS on the backend (FastAPI).
// We set this up in FastAPI earlier, so this should be okay.
const API_BASE_URL = 'http://localhost:8000/api/v1'; // Your backend URL

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    // We can add the Authorization header dynamically later
  },
});

// --- Authentication Endpoints ---

// Login user (expects URL-encoded form data)
export const loginUser = async (email, password) => {
  const params = new URLSearchParams();
  params.append('username', email); // FastAPI's OAuth2 form expects 'username'
  params.append('password', password);

  // Send as x-www-form-urlencoded
  return apiClient.post('/login/token', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
};

// Signup (register) new user
export const signupUser = async (email, password) => {
  return apiClient.post('/users/', { email, password });
};

// Get current user (requires auth token)
export const getCurrentUser = async (token) => {
  return apiClient.get('/users/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};


// --- Add other API functions here later ---
// e.g., getChatbots, createChatbot, etc.


export default apiClient; // Export the configured instance if needed elsewhere