/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type TarefaGantt = {
    /**
     * ID da tarefa
     */
    id: number;
    /**
     * Título da tarefa
     */
    titulo: string;
    /**
     * Data de início da tarefa
     */
    data_inicio: string;
    /**
     * Data de término prevista da tarefa
     */
    data_fim: string;
    /**
     * Percentual de conclusão da tarefa
     */
    progresso: number;
    /**
     * IDs das tarefas das quais esta tarefa depende
     */
    dependencias: Array<number>;
};

