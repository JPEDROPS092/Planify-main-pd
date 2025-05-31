import { useAuth } from '~/composables/useAuth'
import { createFetchClient } from './auth'

/**
 * Serviço para gerenciar permissões de usuário
 */
export const permissionService = {
  /**
   * Busca as permissões do usuário atual
   * @returns Promise com as permissões do usuário
   */
  async getUserPermissions() {
    const api = createFetchClient()

    try {
      const response = await api('/api/users/permissions/', {
        method: 'GET'
      })
      
      return response
    } catch (error) {
      console.error('Erro ao buscar permissões do usuário:', error)
      throw error
    }
  },

  /**
   * Verifica se o usuário tem uma permissão específica
   * @param module Módulo da permissão
   * @param action Ação da permissão
   * @param permissions Lista de permissões do usuário
   * @returns Boolean indicando se o usuário tem a permissão
   */
  hasPermission(module: string, action: string, permissions: string[]) {
    const permissionString = `${module}.${action}`
    return permissions.includes(permissionString)
  }
}

export default permissionService
