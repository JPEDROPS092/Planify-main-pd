/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TarefaKanbanRequest } from './TarefaKanbanRequest';
export type ColunaKanbanRequest = {
    /**
     * Status das tarefas nesta coluna
     */
    status: string;
    /**
     * Título da coluna
     */
    titulo: string;
    /**
     * Lista de tarefas nesta coluna
     */
    tarefas: Array<TarefaKanbanRequest>;
};

