/**
 * Plugin de API para o Planify
 * Configura o cliente Axios global para o Nuxt
 */
import { defineNuxtPlugin } from '#app'
import { getAxiosInstance } from '~/services/api/client/axios'
import { useRuntimeConfig } from '#app'

// Variável para controlar se o plugin já foi inicializado
let initialized = false;

export default defineNuxtPlugin(nuxtApp => {
  // Evitar inicialização múltipla
  if (initialized) {
    console.log('Plugin API já inicializado, pulando...')
    return
  }
  
  // Obter a configuração do Nuxt
  let baseURL = 'http://127.0.0.1:8000'
  try {
    const config = useRuntimeConfig()
    if (config && config.public && config.public.apiBaseUrl) {
      baseURL = config.public.apiBaseUrl
    }
    console.log(`Configurando API com baseURL: ${baseURL}`)
  } catch (e) {
    console.warn("useRuntimeConfig não disponível. Usando baseURL padrão:", baseURL)
  }

  // Obter a instância do Axios com a URL base correta
  const api = getAxiosInstance(baseURL)
  
  // Marcar como inicializado
  initialized = true
  
  // Fornecer a API via provide/inject
  console.log('Plugin API carregado. Cliente Axios configurado com sucesso.')
  
  // Usar apenas um método para fornecer o API
  return {
    provide: {
      api
    }
  }
})
