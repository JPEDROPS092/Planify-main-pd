/**
 * Validação de projetos
 * Funções para validar dados de projetos antes de enviar ao backend
 */
import { Project } from '../../api/endpoints/projects';

/**
 * Interface para erros de validação
 */
export interface ValidationError {
  field: string;
  message: string;
}

/**
 * Valida os dados de um projeto
 * @param project Dados do projeto a validar
 * @returns Array de erros de validação (vazio se válido)
 */
export const validateProject = (project: Partial<Project>): ValidationError[] => {
  const errors: ValidationError[] = [];
  
  // Validar nome do projeto
  if (!project.nome) {
    errors.push({
      field: 'nome',
      message: 'O nome do projeto é obrigatório'
    });
  } else if (project.nome.length < 3) {
    errors.push({
      field: 'nome',
      message: 'O nome do projeto deve ter pelo menos 3 caracteres'
    });
  } else if (project.nome.length > 100) {
    errors.push({
      field: 'nome',
      message: 'O nome do projeto deve ter no máximo 100 caracteres'
    });
  }
  
  // Validar descrição
  if (project.descricao && project.descricao.length > 500) {
    errors.push({
      field: 'descricao',
      message: 'A descrição deve ter no máximo 500 caracteres'
    });
  }
  
  // Validar datas
  if (project.data_inicio && project.data_fim) {
    const startDate = new Date(project.data_inicio);
    const endDate = new Date(project.data_fim);
    
    if (endDate < startDate) {
      errors.push({
        field: 'data_fim',
        message: 'A data de término deve ser posterior à data de início'
      });
    }
  }
  
  // Validar orçamento
  if (project.orcamento !== undefined && project.orcamento !== null) {
    if (isNaN(project.orcamento) || project.orcamento < 0) {
      errors.push({
        field: 'orcamento',
        message: 'O orçamento deve ser um valor numérico positivo'
      });
    }
  }
  
  // Validar status
  if (project.status && !['Planejamento', 'Em andamento', 'Concluído', 'Cancelado', 'Suspenso'].includes(project.status)) {
    errors.push({
      field: 'status',
      message: 'Status inválido'
    });
  }
  
  return errors;
};

/**
 * Verifica se um projeto pode ser excluído
 * @param project Projeto a verificar
 * @returns Objeto com resultado da validação
 */
export const canDeleteProject = (project: Project): { canDelete: boolean; reason?: string } => {
  // Verificar se o projeto tem tarefas
  if (project.tarefas && project.tarefas.length > 0) {
    return {
      canDelete: false,
      reason: 'Não é possível excluir um projeto que possui tarefas. Exclua as tarefas primeiro.'
    };
  }
  
  // Verificar se o projeto está concluído
  if (project.status === 'Concluído') {
    return {
      canDelete: false,
      reason: 'Não é possível excluir um projeto concluído. Altere o status antes de excluir.'
    };
  }
  
  return { canDelete: true };
};

/**
 * Verifica se um projeto pode ser concluído
 * @param project Projeto a verificar
 * @returns Objeto com resultado da validação
 */
export const canCompleteProject = (project: Project): { canComplete: boolean; reason?: string } => {
  // Verificar se todas as tarefas estão concluídas
  if (project.tarefas && project.tarefas.some(tarefa => tarefa.status !== 'Concluída')) {
    return {
      canComplete: false,
      reason: 'Não é possível concluir um projeto com tarefas pendentes.'
    };
  }
  
  // Verificar se há riscos não mitigados
  if (project.riscos && project.riscos.some(risco => !risco.mitigado && risco.impacto === 'Alto')) {
    return {
      canComplete: false,
      reason: 'Existem riscos de alto impacto não mitigados. Recomenda-se mitigá-los antes de concluir o projeto.'
    };
  }
  
  return { canComplete: true };
};
