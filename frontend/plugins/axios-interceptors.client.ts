// plugins/axios-interceptors.client.ts
import axios from 'axios';

export default defineNuxtPlugin(() => {
  let isRefreshing = false;
  let failedQueue: Array<{
    resolve: (value?: any) => void;
    reject: (reason?: any) => void;
  }> = [];

  const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach(({ resolve, reject }) => {
      if (error) {
        reject(error);
      } else {
        resolve(token);
      }
    });
    
    failedQueue = [];
  };

  // Response interceptor for handling global errors and token refresh
  axios.interceptors.response.use(
    (response) => {
      // Return successful responses as-is
      return response;
    },
    async (error) => {
      const originalRequest = error.config;

      // Handle authentication errors
      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          // If already refreshing, queue this request
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject });
          }).then(token => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token;
            return axios(originalRequest);
          }).catch(err => {
            return Promise.reject(err);
          });
        }

        originalRequest._retry = true;
        isRefreshing = true;

        const refreshTokenCookie = useCookie('refresh-token');
        
        if (refreshTokenCookie.value) {
          try {
            const config = useRuntimeConfig();
            const refreshResponse = await axios.post(`${config.public.apiBaseUrl}/api/auth/token/refresh/`, {
              refresh: refreshTokenCookie.value
            });

            if (refreshResponse.data.access) {
              const tokenCookie = useCookie('auth-token');
              tokenCookie.value = refreshResponse.data.access;
              
              // Update refresh token if provided
              if (refreshResponse.data.refresh) {
                refreshTokenCookie.value = refreshResponse.data.refresh;
              }

              // Process queue with new token
              processQueue(null, refreshResponse.data.access);
              
              // Retry original request with new token
              originalRequest.headers['Authorization'] = 'Bearer ' + refreshResponse.data.access;
              return axios(originalRequest);
            }
          } catch (refreshError) {
            console.error('Token refresh failed:', refreshError);
            processQueue(refreshError, null);
            
            // Clear auth cookies
            const tokenCookie = useCookie('auth-token');
            const userCookie = useCookie('auth-user');
            
            tokenCookie.value = null;
            refreshTokenCookie.value = null;
            userCookie.value = null;
            
            // Redirect to login if not already on auth page
            if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/auth')) {
              await navigateTo('/auth/login?expired=true');
            }
          } finally {
            isRefreshing = false;
          }
        } else {
          // No refresh token available, clear auth and redirect
          const tokenCookie = useCookie('auth-token');
          const userCookie = useCookie('auth-user');
          
          tokenCookie.value = null;
          userCookie.value = null;
          
          // Redirect to login if not already on auth page
          if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/auth')) {
            await navigateTo('/auth/login?expired=true');
          }
        }
      }
      
      // Always reject the promise to maintain error handling flow
      return Promise.reject(error);
    }
  );

  // Request interceptor to ensure token is always attached
  axios.interceptors.request.use(
    (config) => {
      // Add token to requests if available
      const tokenCookie = useCookie('auth-token');
      if (tokenCookie.value && !config.headers['Authorization']) {
        config.headers['Authorization'] = `Bearer ${tokenCookie.value}`;
      }
      
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
});
