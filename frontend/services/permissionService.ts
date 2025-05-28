import { useAuth } from '~/composables/useAuth'
import { useNuxtApp } from '#app'

/**
 * Serviço para gerenciar permissões de usuário
 */
export const permissionService = {
  /**
   * Busca as permissões do usuário atual
   * @returns Promise com as permissões do usuário
   */
  async getUserPermissions() {
    const auth = useAuth()
    const accessToken = auth.accessToken
    const { $apiFetch } = useNuxtApp()

    try {
      const response = await $apiFetch('/api/users/permissions/')
      // No need to manually add authorization header as $apiFetch handles that
      
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
