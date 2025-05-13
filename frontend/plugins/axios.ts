import axios from 'axios'
import { ApiError } from '~/services/api'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  
  const api = axios.create({
    baseURL: config.public.apiBaseUrl,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    withCredentials: true // Importante para autenticação com cookies
  })
  
  // Interceptor para adicionar o token de autenticação em cada requisição
  api.interceptors.request.use(config => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })
  
  // Interceptor para tratar erros de resposta
  api.interceptors.response.use(
    response => response,
    async error => {
      const originalRequest = error.config
      
      // Se o erro for 401 (não autorizado) e não for uma tentativa de refresh
      if (error.response && error.response.status === 401 && 
          !originalRequest._retry && 
          !originalRequest.url?.includes('token/refresh')) {
        
        originalRequest._retry = true
        
        // Tentar atualizar o token
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          try {
            const response = await axios.post(`${config.public.apiBaseUrl}/api/auth/token/refresh/`, {
              refresh: refreshToken
            })
            
            if (response.data.access) {
              // Atualizar o token no localStorage
              localStorage.setItem('auth_token', response.data.access)
              
              // Atualizar o header da requisição original
              originalRequest.headers.Authorization = `Bearer ${response.data.access}`
              
              // Reenviar a requisição original
              return axios(originalRequest)
            }
          } catch (refreshError) {
            console.error('Erro ao atualizar token:', refreshError)
            
            // Se falhar ao atualizar o token, redirecionar para login
            localStorage.removeItem('auth_token')
            localStorage.removeItem('refresh_token')
            navigateTo('/login')
          }
        }
        
        // Se não houver refresh token, redirecionar para login
        navigateTo('/login')
      }
      
      // Tratamento padrão de erros
      if (error.response && error.response.status === 401) {
        // Redirecionar para login se não estiver autenticado
        navigateTo('/login')
      }
      
      return Promise.reject(error)
    }
  )
  
  return {
    provide: {
      api
    }
  }
})
