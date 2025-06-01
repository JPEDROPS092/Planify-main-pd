/**
 * Cálculos de métricas de projeto
 * Fornece funções para análise de desempenho e progresso
 */
import { Task } from '../../api/endpoints/tasks';
import { Risk } from '../../api/endpoints/risks';

/**
 * Calcula o percentual de conclusão de um projeto com base nas tarefas
 * @param tasks Lista de tarefas do projeto
 * @returns Percentual de conclusão (0-100)
 */
export const calculateProjectCompletion = (tasks: Task[]): number => {
  if (!tasks.length) return 0;
  
  const completedTasks = tasks.filter(task => task.status === 'Concluída').length;
  return (completedTasks / tasks.length) * 100;
};

/**
 * Calcula o atraso médio das tarefas em dias
 * @param tasks Lista de tarefas do projeto
 * @returns Média de dias de atraso (número positivo)
 */
export const calculateAverageDelay = (tasks: Task[]): number => {
  const delayedTasks = tasks.filter(task => {
    if (!task.data_fim || !task.data_conclusao) return false;
    
    const endDate = new Date(task.data_fim);
    const completionDate = new Date(task.data_conclusao);
    return completionDate > endDate;
  });
  
  if (!delayedTasks.length) return 0;
  
  const totalDelayDays = delayedTasks.reduce((total, task) => {
    const endDate = new Date(task.data_fim!);
    const completionDate = new Date(task.data_conclusao!);
    const delayMs = completionDate.getTime() - endDate.getTime();
    const delayDays = Math.ceil(delayMs / (1000 * 60 * 60 * 24));
    return total + delayDays;
  }, 0);
  
  return totalDelayDays / delayedTasks.length;
};

/**
 * Calcula a distribuição de tarefas por status
 * @param tasks Lista de tarefas do projeto
 * @returns Objeto com contagem de tarefas por status
 */
export const calculateTaskStatusDistribution = (tasks: Task[]): Record<string, number> => {
  const distribution: Record<string, number> = {};
  
  tasks.forEach(task => {
    const status = task.status || 'Sem status';
    distribution[status] = (distribution[status] || 0) + 1;
  });
  
  return distribution;
};

/**
 * Calcula a distribuição de tarefas por membro da equipe
 * @param tasks Lista de tarefas do projeto
 * @returns Objeto com contagem de tarefas por membro
 */
export const calculateTasksByMember = (tasks: Task[]): Record<string, number> => {
  const distribution: Record<string, number> = {};
  
  tasks.forEach(task => {
    if (task.responsavel) {
      const memberName = typeof task.responsavel === 'object' 
        ? `${task.responsavel.first_name} ${task.responsavel.last_name}`.trim() || task.responsavel.username
        : `Membro ${task.responsavel}`;
        
      distribution[memberName] = (distribution[memberName] || 0) + 1;
    } else {
      distribution['Sem responsável'] = (distribution['Sem responsável'] || 0) + 1;
    }
  });
  
  return distribution;
};

/**
 * Calcula a pontuação de risco do projeto
 * @param risks Lista de riscos do projeto
 * @returns Pontuação de risco (quanto maior, mais arriscado)
 */
export const calculateRiskScore = (risks: Risk[]): number => {
  if (!risks.length) return 0;
  
  // Pesos para cada nível de impacto
  const impactWeights: Record<string, number> = {
    'Baixo': 1,
    'Médio': 2,
    'Alto': 3,
    'Crítico': 5
  };
  
  // Pesos para cada probabilidade
  const probabilityWeights: Record<string, number> = {
    'Muito baixa': 1,
    'Baixa': 2,
    'Média': 3,
    'Alta': 4,
    'Muito alta': 5
  };
  
  // Calcular pontuação total
  const totalScore = risks.reduce((score, risk) => {
    const impactWeight = impactWeights[risk.impacto || 'Médio'] || 2;
    const probabilityWeight = probabilityWeights[risk.probabilidade || 'Média'] || 3;
    
    // Riscos mitigados têm peso reduzido
    const mitigationFactor = risk.mitigado ? 0.3 : 1;
    
    return score + (impactWeight * probabilityWeight * mitigationFactor);
  }, 0);
  
  return totalScore;
};

/**
 * Calcula a taxa de conclusão de tarefas dentro do prazo
 * @param tasks Lista de tarefas concluídas
 * @returns Percentual de tarefas concluídas no prazo (0-100)
 */
export const calculateOnTimeCompletionRate = (tasks: Task[]): number => {
  const completedTasks = tasks.filter(task => 
    task.status === 'Concluída' && task.data_conclusao
  );
  
  if (!completedTasks.length) return 0;
  
  const onTimeTasks = completedTasks.filter(task => {
    const endDate = new Date(task.data_fim!);
    const completionDate = new Date(task.data_conclusao!);
    return completionDate <= endDate;
  });
  
  return (onTimeTasks.length / completedTasks.length) * 100;
};

/**
 * Calcula a velocidade da equipe (tarefas concluídas por período)
 * @param tasks Lista de tarefas concluídas
 * @param periodDays Número de dias no período
 * @returns Média de tarefas concluídas por período
 */
export const calculateTeamVelocity = (tasks: Task[], periodDays: number = 7): number => {
  const completedTasks = tasks.filter(task => 
    task.status === 'Concluída' && task.data_conclusao
  );
  
  if (!completedTasks.length) return 0;
  
  // Encontrar a data mais antiga e mais recente
  const dates = completedTasks.map(task => new Date(task.data_conclusao!).getTime());
  const oldestDate = new Date(Math.min(...dates));
  const newestDate = new Date(Math.max(...dates));
  
  // Calcular o número de períodos
  const totalDays = (newestDate.getTime() - oldestDate.getTime()) / (1000 * 60 * 60 * 24);
  const periods = Math.max(1, totalDays / periodDays);
  
  return completedTasks.length / periods;
};
