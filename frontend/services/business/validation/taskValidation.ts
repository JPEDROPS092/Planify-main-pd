/**
 * Validação de tarefas
 * Funções para validar dados de tarefas antes de enviar ao backend
 */
import { Task } from '../../api/endpoints/tasks';
import { ValidationError } from './projectValidation';

/**
 * Valida os dados de uma tarefa
 * @param task Dados da tarefa a validar
 * @returns Array de erros de validação (vazio se válido)
 */
export const validateTask = (task: Partial<Task>): ValidationError[] => {
  const errors: ValidationError[] = [];
  
  // Validar título da tarefa
  if (!task.titulo) {
    errors.push({
      field: 'titulo',
      message: 'O título da tarefa é obrigatório'
    });
  } else if (task.titulo.length < 3) {
    errors.push({
      field: 'titulo',
      message: 'O título da tarefa deve ter pelo menos 3 caracteres'
    });
  } else if (task.titulo.length > 100) {
    errors.push({
      field: 'titulo',
      message: 'O título da tarefa deve ter no máximo 100 caracteres'
    });
  }
  
  // Validar descrição
  if (task.descricao && task.descricao.length > 500) {
    errors.push({
      field: 'descricao',
      message: 'A descrição deve ter no máximo 500 caracteres'
    });
  }
  
  // Validar projeto
  if (!task.projeto) {
    errors.push({
      field: 'projeto',
      message: 'A tarefa deve estar associada a um projeto'
    });
  }
  
  // Validar datas
  if (task.data_inicio && task.data_fim) {
    const startDate = new Date(task.data_inicio);
    const endDate = new Date(task.data_fim);
    
    if (endDate < startDate) {
      errors.push({
        field: 'data_fim',
        message: 'A data de término deve ser posterior à data de início'
      });
    }
  }
  
  // Validar prioridade
  if (task.prioridade && !['Baixa', 'Média', 'Alta', 'Urgente'].includes(task.prioridade)) {
    errors.push({
      field: 'prioridade',
      message: 'Prioridade inválida'
    });
  }
  
  // Validar status
  if (task.status && !['Pendente', 'Em andamento', 'Em revisão', 'Concluída', 'Cancelada'].includes(task.status)) {
    errors.push({
      field: 'status',
      message: 'Status inválido'
    });
  }
  
  // Validar estimativa de horas
  if (task.estimativa_horas !== undefined && task.estimativa_horas !== null) {
    if (isNaN(task.estimativa_horas) || task.estimativa_horas < 0) {
      errors.push({
        field: 'estimativa_horas',
        message: 'A estimativa de horas deve ser um valor numérico positivo'
      });
    }
  }
  
  // Validar horas trabalhadas
  if (task.horas_trabalhadas !== undefined && task.horas_trabalhadas !== null) {
    if (isNaN(task.horas_trabalhadas) || task.horas_trabalhadas < 0) {
      errors.push({
        field: 'horas_trabalhadas',
        message: 'As horas trabalhadas devem ser um valor numérico positivo'
      });
    }
  }
  
  return errors;
};

/**
 * Verifica se uma tarefa pode ser marcada como concluída
 * @param task Tarefa a verificar
 * @returns Objeto com resultado da validação
 */
export const canCompleteTask = (task: Task): { canComplete: boolean; reason?: string } => {
  // Verificar se a tarefa tem responsável
  if (!task.responsavel) {
    return {
      canComplete: false,
      reason: 'Não é possível concluir uma tarefa sem responsável.'
    };
  }
  
  // Verificar se a tarefa tem subtarefas não concluídas
  if (task.subtarefas && task.subtarefas.some(subtarefa => subtarefa.status !== 'Concluída')) {
    return {
      canComplete: false,
      reason: 'Não é possível concluir uma tarefa com subtarefas pendentes.'
    };
  }
  
  return { canComplete: true };
};

/**
 * Verifica se uma tarefa pode ser excluída
 * @param task Tarefa a verificar
 * @returns Objeto com resultado da validação
 */
export const canDeleteTask = (task: Task): { canDelete: boolean; reason?: string } => {
  // Verificar se a tarefa tem subtarefas
  if (task.subtarefas && task.subtarefas.length > 0) {
    return {
      canDelete: false,
      reason: 'Não é possível excluir uma tarefa que possui subtarefas. Exclua as subtarefas primeiro.'
    };
  }
  
  // Verificar se a tarefa está concluída há mais de 30 dias
  if (task.status === 'Concluída' && task.data_conclusao) {
    const completionDate = new Date(task.data_conclusao);
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    if (completionDate < thirtyDaysAgo) {
      return {
        canDelete: false,
        reason: 'Não é possível excluir uma tarefa concluída há mais de 30 dias.'
      };
    }
  }
  
  return { canDelete: true };
};

/**
 * Verifica se uma tarefa está atrasada
 * @param task Tarefa a verificar
 * @returns Verdadeiro se a tarefa estiver atrasada
 */
export const isTaskOverdue = (task: Task): boolean => {
  if (!task.data_fim || task.status === 'Concluída' || task.status === 'Cancelada') {
    return false;
  }
  
  const endDate = new Date(task.data_fim);
  const today = new Date();
  
  // Remover horas, minutos e segundos para comparação apenas de datas
  endDate.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);
  
  return endDate < today;
};
