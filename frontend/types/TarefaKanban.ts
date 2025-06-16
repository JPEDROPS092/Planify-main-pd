/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type TarefaKanban = {
    /**
     * ID da tarefa
     */
    id: number;
    /**
     * Título da tarefa
     */
    titulo: string;
    /**
     * Descrição da tarefa
     */
    descricao: string;
    /**
     * Status atual da tarefa
     */
    status: string;
    /**
     * Prioridade da tarefa
     */
    prioridade: string;
    /**
     * Data de início da tarefa
     */
    data_inicio: string;
    /**
     * Data de término prevista da tarefa
     */
    data_fim: string;
    /**
     * Lista de usuários responsáveis pela tarefa
     */
    responsaveis: Array<Record<string, any>>;
};

