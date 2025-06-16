/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ProjetoDashboardResponse = {
    /**
     * Detalhes do projeto
     */
    projeto: Record<string, any>;
    /**
     * Lista de sprints do projeto
     */
    sprints: Array<any>;
    /**
     * Tarefas agrupadas por status para visualização Kanban
     */
    tarefas_kanban: Record<string, any>;
    /**
     * Métricas do projeto
     */
    metricas: Record<string, any>;
    /**
     * Atividades recentes no projeto
     */
    atividades_recentes: Array<any>;
};

