/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContadorTarefaStatus } from './ContadorTarefaStatus';
import type { ProximaTarefa } from './ProximaTarefa';
/**
 * Serializador para dashboard pessoal do usuário.
 */
export type DashboardUsuario = {
    /**
     * Número de projetos onde o usuário é o gerente
     */
    projetos_gerenciados: number;
    /**
     * Contagem das tarefas do usuário, agrupadas por status
     */
    tarefas_por_status: Array<ContadorTarefaStatus>;
    /**
     * Número de tarefas atribuídas ao usuário que estão atrasadas
     */
    tarefas_atrasadas: number;
    /**
     * Lista das próximas tarefas agendadas para o usuário
     */
    proximas_tarefas: Array<ProximaTarefa>;
};

