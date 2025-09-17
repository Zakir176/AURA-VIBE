// src/utils/auth.js

const TOKEN_KEY = "aura_vibe_token";
const USER_KEY = "aura_vibe_user";

/**
 * Save token & user data to localStorage
 */
export function setAuth(token, user = {}) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

/**
 * Get saved auth token
 */
export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Get saved user data
 */
export function getUser() {
  const user = localStorage.getItem(USER_KEY);
  return user ? JSON.parse(user) : null;
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated() {
  return !!getToken();
}

/**
 * Clear token & user data (logout)
 */
export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}
