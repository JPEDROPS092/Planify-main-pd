/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContadorTarefaStatus } from './ContadorTarefaStatus';
/**
 * Serializador para métricas detalhadas de um projeto específico.
 */
export type MetricasProjeto = {
    /**
     * Contagem de tarefas do projeto, agrupadas por status
     */
    tarefas_por_status: Array<ContadorTarefaStatus>;
    /**
     * Percentual de conclusão do projeto (0-100)
     */
    progresso: number;
    /**
     * Número de riscos atualmente ativos para o projeto
     */
    riscos_ativos: number;
    /**
     * Soma dos custos registrados para o projeto
     */
    custos_totais: number;
    /**
     * Número de dias restantes até a data final planejada do projeto
     */
    dias_restantes: number;
};

