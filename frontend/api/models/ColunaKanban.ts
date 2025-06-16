/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TarefaKanban } from './TarefaKanban';
export type ColunaKanban = {
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
    tarefas: Array<TarefaKanban>;
};

