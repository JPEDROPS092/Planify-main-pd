import { useApiService } from './api'

export interface User {
  id?: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  full_name?: string
  is_active?: boolean
  is_staff?: boolean
  date_joined?: string
  last_login?: string
  profile_picture?: string | File
}

export const useUserService = () => {
  const api = useApiService()
  const endpoint = '/api/auth/users/'

  // Listar todos os usuários
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter um usuário específico
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter o usuário atual
  const getCurrentUser = async () => {
    try {
      const response = await api.get(`${endpoint}me/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar um novo usuário
  const create = async (user: User) => {
    try {
      // Se houver uma imagem de perfil, usamos FormData
      if (user.profile_picture && user.profile_picture instanceof File) {
        const formData = new FormData()
        Object.keys(user).forEach(key => {
          if (key === 'profile_picture') {
            formData.append(key, user[key])
          } else {
            formData.append(key, user[key])
          }
        })
        
        const response = await api.post(endpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.post(endpoint, user)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Atualizar um usuário existente
  const update = async (id: number, user: User) => {
    try {
      // Se houver uma imagem de perfil, usamos FormData
      if (user.profile_picture && user.profile_picture instanceof File) {
        const formData = new FormData()
        Object.keys(user).forEach(key => {
          if (key === 'profile_picture') {
            formData.append(key, user[key])
          } else {
            formData.append(key, user[key])
          }
        })
        
        const response = await api.put(`${endpoint}${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.put(`${endpoint}${id}/`, user)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente um usuário
  const patch = async (id: number, partialUser: Partial<User>) => {
    try {
      // Se houver uma imagem de perfil, usamos FormData
      if (partialUser.profile_picture && partialUser.profile_picture instanceof File) {
        const formData = new FormData()
        Object.keys(partialUser).forEach(key => {
          if (key === 'profile_picture') {
            formData.append(key, partialUser[key])
          } else {
            formData.append(key, partialUser[key])
          }
        })
        
        const response = await api.patch(`${endpoint}${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.patch(`${endpoint}${id}/`, partialUser)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Atualizar o usuário atual
  const updateCurrentUser = async (userData: Partial<User>) => {
    try {
      // Se houver uma imagem de perfil, usamos FormData
      if (userData.profile_picture && userData.profile_picture instanceof File) {
        const formData = new FormData()
        Object.keys(userData).forEach(key => {
          if (key === 'profile_picture') {
            formData.append(key, userData[key])
          } else {
            formData.append(key, userData[key])
          }
        })
        
        const response = await api.patch(`${endpoint}me/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.patch(`${endpoint}me/`, userData)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Alterar senha do usuário atual
  const changePassword = async (currentPassword: string, newPassword: string) => {
    try {
      const response = await api.post(`${endpoint}set_password/`, {
        current_password: currentPassword,
        new_password: newPassword
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Desativar um usuário
  const deactivate = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { is_active: false })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Ativar um usuário
  const activate = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { is_active: true })
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    getAll,
    getById,
    getCurrentUser,
    create,
    update,
    patch,
    updateCurrentUser,
    changePassword,
    deactivate,
    activate
  }
}
