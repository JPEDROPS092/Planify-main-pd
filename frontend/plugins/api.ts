/**
 * Plugin de API para o Planify
 * Configura e disponibiliza o cliente Axios para toda a aplicação
 */
import { defineNuxtPlugin } from '#app'
import axios from 'axios'
import { setupInterceptors } from '~/services/api/client/interceptors'

export default defineNuxtPlugin(nuxtApp => {
  const config = useRuntimeConfig()
  const accessToken = useState<string | null>('auth.accessToken')

  // Criar instância do Axios com configurações padrão
  const api = axios.create({
    baseURL: config.public.apiBaseUrl || 'http://localhost:8000',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    withCredentials: true // Importante para autenticação com cookies
  })

  // Configurar interceptores para a instância da API
  setupInterceptors(api)

  // Disponibilizar a instância da API globalmente via $api
  nuxtApp.provide('api', api)

  console.log('Plugin API carregado. Cliente Axios configurado com sucesso.')

  return {
    provide: {
      api
    }
  }
})
