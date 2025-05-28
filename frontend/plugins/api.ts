import { defineNuxtPlugin } from '#app'

export default defineNuxtPlugin((nuxtApp) => {
  // Only override fetch for API calls, not for Nuxt internal resources
  const customFetch = (url, options = {}) => {
    // Check if this is a Nuxt internal resource request
    const isNuxtResource = url.includes('/_nuxt/') || 
                         url.includes('/__nuxt_island/') || 
                         url.includes('/builds/meta/') ||
                         url.startsWith('/_ipx/') ||
                         url.includes('/__nuxt/');

    // For Nuxt resources, use the default fetch without additional options
    if (isNuxtResource) {
      return $fetch(url, options);
    }

    // For API requests, add authentication and other options
    const apiOptions = {
      ...options,
      baseURL: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      credentials: 'include',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...options.headers
      },
      onRequest({ request, options }) {
        // Add authentication token for API requests
        if (process.client) {
          const token = localStorage.getItem('auth_token')
          if (token) {
            options.headers = {
              ...options.headers,
              Authorization: `Bearer ${token}`
            }
          }
        }
      },
      onResponseError({ request, response, options }) {
        // Handle authentication errors, but only for API requests
        if (response?.status === 401 && !request.toString().includes('/api/auth/token/')) {
          if (process.client) {
            localStorage.removeItem('auth_token')
            localStorage.removeItem('refresh_token')
            window.location.href = '/login'
          }
        }
      }
    };

    return $fetch(url, apiOptions);
  };

  // Provide a custom fetcher but don't override the global one
  // This prevents interference with Nuxt's internal fetch operations
  nuxtApp.provide('apiFetch', customFetch);
})
