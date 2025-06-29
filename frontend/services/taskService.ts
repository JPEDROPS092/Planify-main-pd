// Stub service para tarefas - temporário até a integração completa com Orval
export interface Task {
  id: string
  titulo: string
  descricao?: string
  status: 'pendente' | 'em_andamento' | 'concluida' | 'cancelada'
  prioridade: 'baixa' | 'media' | 'alta' | 'critica'
  dataVencimento?: string
  dataCriacao: string
  atribuido?: {
    id: string
    nome: string
    email: string
  }
  projeto?: {
    id: string
    nome: string
  }
}

export interface CreateTaskDto {
  titulo: string
  descricao?: string
  prioridade: Task['prioridade']
  dataVencimento?: string
  projetoId?: string
  atribuidoId?: string
}

export interface UpdateTaskDto extends Partial<CreateTaskDto> {
  status?: Task['status']
}

// Mock data para demonstração
const mockTasks: Task[] = [
  {
    id: '1',
    titulo: 'Implementar autenticação',
    descricao: 'Criar sistema de login e registro de usuários',
    status: 'em_andamento',
    prioridade: 'alta',
    dataVencimento: '2024-01-20',
    dataCriacao: '2024-01-10',
    atribuido: {
      id: '1',
      nome: 'João Silva',
      email: 'joao@example.com'
    },
    projeto: {
      id: '1',
      nome: 'Planify Frontend'
    }
  },
  {
    id: '2',
    titulo: 'Configurar CI/CD',
    descricao: 'Configurar pipeline de deploy automático',
    status: 'pendente',
    prioridade: 'media',
    dataVencimento: '2024-01-25',
    dataCriacao: '2024-01-12',
    projeto: {
      id: '1',
      nome: 'Planify Frontend'
    }
  },
  {
    id: '3',
    titulo: 'Testes unitários',
    descricao: 'Implementar testes para componentes principais',
    status: 'concluida',
    prioridade: 'baixa',
    dataCriacao: '2024-01-08',
    atribuido: {
      id: '2',
      nome: 'Maria Santos',
      email: 'maria@example.com'
    }
  }
]

// Simular delay de API
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export class TaskService {
  static async getAllTasks(): Promise<Task[]> {
    await delay(500) // Simular latência da API
    return [...mockTasks]
  }

  static async getTaskById(id: string): Promise<Task | null> {
    await delay(300)
    return mockTasks.find(task => task.id === id) || null
  }

  static async createTask(taskData: CreateTaskDto): Promise<Task> {
    await delay(600)
    
    const newTask: Task = {
      id: (mockTasks.length + 1).toString(),
      ...taskData,
      status: 'pendente',
      dataCriacao: new Date().toISOString().split('T')[0]
    }
    
    mockTasks.push(newTask)
    return newTask
  }

  static async updateTask(id: string, updates: UpdateTaskDto): Promise<Task | null> {
    await delay(400)
    
    const taskIndex = mockTasks.findIndex(task => task.id === id)
    if (taskIndex === -1) return null
    
    mockTasks[taskIndex] = { ...mockTasks[taskIndex], ...updates }
    return mockTasks[taskIndex]
  }

  static async deleteTask(id: string): Promise<boolean> {
    await delay(300)
    
    const taskIndex = mockTasks.findIndex(task => task.id === id)
    if (taskIndex === -1) return false
    
    mockTasks.splice(taskIndex, 1)
    return true
  }

  static async getTasksByProject(projectId: string): Promise<Task[]> {
    await delay(400)
    return mockTasks.filter(task => task.projeto?.id === projectId)
  }

  static async getTasksByUser(userId: string): Promise<Task[]> {
    await delay(400)
    return mockTasks.filter(task => task.atribuido?.id === userId)
  }
}

// Hook para uso com Vue Query (quando disponível)
export function useTaskService() {
  return {
    getAllTasks: TaskService.getAllTasks,
    getTaskById: TaskService.getTaskById,
    createTask: TaskService.createTask,
    updateTask: TaskService.updateTask,
    deleteTask: TaskService.deleteTask,
    getTasksByProject: TaskService.getTasksByProject,
    getTasksByUser: TaskService.getTasksByUser
  }
}
