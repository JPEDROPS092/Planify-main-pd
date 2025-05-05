import axios from 'axios'

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
    error => {
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
