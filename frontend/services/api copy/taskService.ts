/**
 * Serviço de tarefas - adaptador para o novo sistema de API
 */
import { ref, computed } from 'vue'
import * as tasksApi from '~/services/api/tasks'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'

export const useTaskService = () => {
  const { user, hasPermission } = useAuth()
  const { handleApiError, withLoading } = useApiService()
  
  const tasks = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Tarefas filtradas para o usuário atual
  const myTasks = computed(() => {
    if (!user.value || !tasks.value) return []
    return tasks.value.filter(task => 
      task.assigned_to?.id === user.value.id
    )
  })
  
  // Carregar todas as tarefas
  const fetchTasks = async (projectId = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      if (projectId) {
        tasks.value = await tasksApi.listTasksByProject(projectId)
      } else {
        tasks.value = await tasksApi.listTasks()
      }
      return tasks.value
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter uma tarefa pelo ID
  const getTask = async (taskId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const task = await tasksApi.retrieveTask(taskId)
      return task
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Criar uma nova tarefa
  const createTask = async (taskData) => {
    return withLoading(async () => {
      try {
        // Associar automaticamente o usuário atual como criador se não estiver definido
        if (!taskData.created_by) {
          taskData.created_by = user.value?.id
        }
        
        const newTask = await tasksApi.createTask(taskData)
        tasks.value = [...tasks.value, newTask]
        return newTask
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar uma tarefa
  const updateTask = async (taskId, taskData) => {
    return withLoading(async () => {
      try {
        const updatedTask = await tasksApi.updateTask(taskId, taskData)
        
        // Atualizar a lista local
        tasks.value = tasks.value.map(task => 
          task.id === taskId ? updatedTask : task
        )
        
        return updatedTask
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Excluir uma tarefa
  const deleteTask = async (taskId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('task', 'delete')) {
          throw new Error('Você não tem permissão para excluir esta tarefa')
        }
        
        await tasksApi.destroyTask(taskId)
        
        // Remover da lista local
        tasks.value = tasks.value.filter(task => task.id !== taskId)
        
        return true
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar status de uma tarefa
  const updateTaskStatus = async (taskId, status) => {
    return withLoading(async () => {
      try {
        const updatedTask = await tasksApi.updateTaskStatus(taskId, { status })
        
        // Atualizar a lista local
        tasks.value = tasks.value.map(task => 
          task.id === taskId ? updatedTask : task
        )
        
        return updatedTask
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Adicionar comentário a uma tarefa
  const addTaskComment = async (taskId, commentData) => {
    return withLoading(async () => {
      try {
        const updatedTask = await tasksApi.addTaskComment(taskId, commentData)
        
        // Atualizar a lista local
        tasks.value = tasks.value.map(task => 
          task.id === taskId ? updatedTask : task
        )
        
        return updatedTask
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  return {
    tasks,
    myTasks,
    isLoading,
    error,
    fetchTasks,
    getTask,
    createTask,
    updateTask,
    deleteTask,
    updateTaskStatus,
    addTaskComment
  }
}
