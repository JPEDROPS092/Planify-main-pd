/**
 * Serviço de comunicações do Planify
 * Fornece funções para gerenciamento de mensagens e notificações
 */
import { ref } from 'vue'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'
import * as api from './communications'
import type {
  ChatMensagem,
  ChatMensagemRequest,
  Notificacao,
  NotificacaoRequest,
  PaginatedResponse
} from './types'

/**
 * Composable para gerenciamento de mensagens de chat
 * Fornece estado reativo e métodos para gerenciar mensagens
 */
export const useChatService = () => {
  const { handleApiError, withLoading } = useApiService()
  const { user } = useAuth()
  
  const mensagens = ref<ChatMensagem[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  /**
   * Carrega mensagens de um projeto
   * @param projetoId ID do projeto
   * @param params Parâmetros adicionais
   * @returns Lista de mensagens
   */
  const fetchMensagens = async (projetoId: number, params?: { page?: number, ordering?: string }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.listMensagens({
        projeto: projetoId,
        ...params
      })
      mensagens.value = response.results
      return response
    } catch (err: any) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Envia uma nova mensagem
   * @param mensagemData Dados da mensagem
   * @returns Mensagem criada
   */
  const enviarMensagem = async (mensagemData: ChatMensagemRequest) => {
    return withLoading(
      async () => {
        try {
          const novaMensagem = await api.createMensagem(mensagemData)
          mensagens.value = [...mensagens.value, novaMensagem]
          return novaMensagem
        } catch (err: any) {
          error.value = handleApiError(err)
          throw err
        }
      },
      { 
        loadingMessage: 'Enviando mensagem...',
        successMessage: 'Mensagem enviada com sucesso!'
      }
    )
  }
  
  /**
   * Marca uma mensagem como lida
   * @param mensagemId ID da mensagem
   * @returns Mensagem atualizada
   */
  const marcarComoLida = async (mensagemId: number) => {
    try {
      const mensagemAtualizada = await api.marcarComoLidaMensagem(mensagemId)
      
      // Atualiza a mensagem na lista
      mensagens.value = mensagens.value.map(m => 
        m.id === mensagemId ? mensagemAtualizada : m
      )
      
      return mensagemAtualizada
    } catch (err: any) {
      error.value = handleApiError(err)
      throw err
    }
  }
  
  /**
   * Obtém mensagens não lidas
   * @returns Lista de mensagens não lidas
   */
  const getMensagensNaoLidas = async () => {
    try {
      return await api.retrieveMensagensNaoLidas()
    } catch (err: any) {
      error.value = handleApiError(err)
      throw err
    }
  }
  
  /**
   * Exclui uma mensagem
   * @param mensagemId ID da mensagem
   * @returns void
   */
  const excluirMensagem = async (mensagemId: number) => {
    return withLoading(
      async () => {
        try {
          await api.destroyMensagem(mensagemId)
          
          // Remove a mensagem da lista
          mensagens.value = mensagens.value.filter(m => m.id !== mensagemId)
          
          return true
        } catch (err: any) {
          error.value = handleApiError(err)
          throw err
        }
      },
      {
        loadingMessage: 'Excluindo mensagem...',
        successMessage: 'Mensagem excluída com sucesso!'
      }
    )
  }
  
  return {
    mensagens,
    isLoading,
    error,
    fetchMensagens,
    enviarMensagem,
    marcarComoLida,
    getMensagensNaoLidas,
    excluirMensagem
  }
}

/**
 * Composable para gerenciamento de notificações
 * Fornece estado reativo e métodos para gerenciar notificações
 */
export const useNotificationService = () => {
  const { handleApiError, withLoading } = useApiService()
  const { user } = useAuth()
  
  const notificacoes = ref<Notificacao[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  /**
   * Carrega notificações do usuário atual
   * @param params Parâmetros adicionais
   * @returns Lista paginada de notificações
   */
  const fetchNotificacoes = async (params?: { page?: number, lida?: boolean, ordering?: string }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const userId = user.value?.id
      if (!userId) {
        throw new Error('Usuário não autenticado')
      }
      
      const response = await api.listNotificacoes({
        usuario: userId,
        ...params
      })
      
      notificacoes.value = response.results
      return response
    } catch (err: any) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Marca uma notificação como lida
   * @param notificacaoId ID da notificação
   * @returns Notificação atualizada
   */
  const marcarComoLida = async (notificacaoId: number) => {
    try {
      const notificacaoAtualizada = await api.marcarComoLidaNotificacao(notificacaoId)
      
      // Atualiza a notificação na lista
      notificacoes.value = notificacoes.value.map(n => 
        n.id === notificacaoId ? notificacaoAtualizada : n
      )
      
      return notificacaoAtualizada
    } catch (err: any) {
      error.value = handleApiError(err)
      throw err
    }
  }
  
  /**
   * Marca todas as notificações como lidas
   * @returns void
   */
  const marcarTodasComoLidas = async () => {
    return withLoading(
      async () => {
        try {
          await api.marcarTodasComoLidasNotificacoes()
          
          // Atualiza todas as notificações na lista como lidas
          notificacoes.value = notificacoes.value.map(n => ({
            ...n,
            lida: true
          }))
          
          return true
        } catch (err: any) {
          error.value = handleApiError(err)
          throw err
        }
      },
      {
        loadingMessage: 'Marcando notificações como lidas...',
        successMessage: 'Todas as notificações foram marcadas como lidas!'
      }
    )
  }
  
  /**
   * Exclui uma notificação
   * @param notificacaoId ID da notificação
   * @returns void
   */
  const excluirNotificacao = async (notificacaoId: number) => {
    return withLoading(
      async () => {
        try {
          await api.destroyNotificacao(notificacaoId)
          
          // Remove a notificação da lista
          notificacoes.value = notificacoes.value.filter(n => n.id !== notificacaoId)
          
          return true
        } catch (err: any) {
          error.value = handleApiError(err)
          throw err
        }
      },
      {
        loadingMessage: 'Excluindo notificação...',
        successMessage: 'Notificação excluída com sucesso!'
      }
    )
  }
  
  return {
    notificacoes,
    isLoading,
    error,
    fetchNotificacoes,
    marcarComoLida,
    marcarTodasComoLidas,
    excluirNotificacao
  }
}
