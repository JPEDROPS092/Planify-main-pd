// Stub service para usuários - temporário até a integração completa com Orval
export interface User {
  id: string
  nome: string
  email: string
  ativo: boolean
  dataCadastro: string
  avatar?: string
  telefone?: string
  cargo?: string
  departamento?: string
}

export interface CreateUserDto {
  nome: string
  email: string
  senha: string
  telefone?: string
  cargo?: string
  departamento?: string
}

export interface UpdateUserDto {
  nome?: string
  email?: string
  telefone?: string
  cargo?: string
  departamento?: string
  ativo?: boolean
}

export interface UserListParams {
  page?: number
  limit?: number
  search?: string
  ativo?: boolean
  departamento?: string
}

export interface UserListResponse {
  users: User[]
  total: number
  page: number
  limit: number
  totalPages: number
}

// Mock data para demonstração
const mockUsers: User[] = [
  {
    id: '1',
    nome: 'João Silva',
    email: 'joao@example.com',
    ativo: true,
    dataCadastro: '2024-01-10',
    cargo: 'Desenvolvedor Full Stack',
    departamento: 'Tecnologia'
  },
  {
    id: '2',
    nome: 'Maria Santos',
    email: 'maria@example.com',
    ativo: true,
    dataCadastro: '2024-01-08',
    cargo: 'Product Manager',
    departamento: 'Produto'
  },
  {
    id: '3',
    nome: 'Pedro Costa',
    email: 'pedro@example.com',
    ativo: false,
    dataCadastro: '2024-01-05',
    cargo: 'Designer UI/UX',
    departamento: 'Design'
  }
]

// Simular delay de API
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export class UserService {
  static async getUsers(params: UserListParams = {}): Promise<UserListResponse> {
    await delay(500)
    
    const { page = 1, limit = 10, search = '', ativo, departamento } = params
    
    let filteredUsers = [...mockUsers]
    
    if (search) {
      filteredUsers = filteredUsers.filter(user => 
        user.nome.toLowerCase().includes(search.toLowerCase()) ||
        user.email.toLowerCase().includes(search.toLowerCase())
      )
    }
    
    if (ativo !== undefined) {
      filteredUsers = filteredUsers.filter(user => user.ativo === ativo)
    }
    
    if (departamento) {
      filteredUsers = filteredUsers.filter(user => user.departamento === departamento)
    }
    
    const startIndex = (page - 1) * limit
    const endIndex = startIndex + limit
    const users = filteredUsers.slice(startIndex, endIndex)
    
    return {
      users,
      total: filteredUsers.length,
      page,
      limit,
      totalPages: Math.ceil(filteredUsers.length / limit)
    }
  }

  static async getUser(id: string): Promise<User | null> {
    await delay(300)
    return mockUsers.find(user => user.id === id) || null
  }

  static async createUser(userData: CreateUserDto): Promise<User> {
    await delay(600)
    
    const newUser: User = {
      id: (mockUsers.length + 1).toString(),
      nome: userData.nome,
      email: userData.email,
      ativo: true,
      dataCadastro: new Date().toISOString().split('T')[0],
      telefone: userData.telefone,
      cargo: userData.cargo,
      departamento: userData.departamento
    }
    
    mockUsers.push(newUser)
    return newUser
  }

  static async updateUser(id: string, updates: UpdateUserDto): Promise<User | null> {
    await delay(400)
    
    const userIndex = mockUsers.findIndex(user => user.id === id)
    if (userIndex === -1) return null
    
    mockUsers[userIndex] = { ...mockUsers[userIndex], ...updates }
    return mockUsers[userIndex]
  }

  static async patchUser(id: string, updates: Partial<UpdateUserDto>): Promise<User | null> {
    return this.updateUser(id, updates)
  }

  static async deleteUser(id: string): Promise<boolean> {
    await delay(300)
    
    const userIndex = mockUsers.findIndex(user => user.id === id)
    if (userIndex === -1) return false
    
    mockUsers.splice(userIndex, 1)
    return true
  }

  static async activateUser(id: string): Promise<boolean> {
    await delay(300)
    
    const user = mockUsers.find(user => user.id === id)
    if (!user) return false
    
    user.ativo = true
    return true
  }

  static async deactivateUser(id: string): Promise<boolean> {
    await delay(300)
    
    const user = mockUsers.find(user => user.id === id)
    if (!user) return false
    
    user.ativo = false
    return true
  }

  static async resetPassword(id: string): Promise<boolean> {
    await delay(500)
    
    const user = mockUsers.find(user => user.id === id)
    return !!user // Simula sucesso se o usuário existe
  }
}

// Hook para uso com Vue Query
export function useUserService() {
  return {
    getUsers: UserService.getUsers,
    getUser: UserService.getUser,
    createUser: UserService.createUser,
    updateUser: UserService.updateUser,
    patchUser: UserService.patchUser,
    deleteUser: UserService.deleteUser,
    activateUser: UserService.activateUser,
    deactivateUser: UserService.deactivateUser,
    resetPassword: UserService.resetPassword
  }
}

// Export direto do service para compatibilidade
export const userService = {
  getUsers: UserService.getUsers,
  getUser: UserService.getUser,
  createUser: UserService.createUser,
  updateUser: UserService.updateUser,
  patchUser: UserService.patchUser,
  deleteUser: UserService.deleteUser,
  activateUser: UserService.activateUser,
  deactivateUser: UserService.deactivateUser,
  resetPassword: UserService.resetPassword
}
