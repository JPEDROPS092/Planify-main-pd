/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContadorTarefaStatus } from './ContadorTarefaStatus';
/**
 * Serializador para visão geral do dashboard do sistema.
 */
export type VisaoGeralDashboard = {
    /**
     * Número total de projetos no sistema
     */
    total_projetos: number;
    /**
     * Número total de tarefas no sistema
     */
    total_tarefas: number;
    /**
     * Lista detalhada da contagem de tarefas por cada status
     */
    tarefas_por_status: Array<ContadorTarefaStatus>;
};

