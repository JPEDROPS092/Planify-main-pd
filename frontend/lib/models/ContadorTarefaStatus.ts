/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializador para contagem de tarefas por status.
 */
export type ContadorTarefaStatus = {
    /**
     * Status da tarefa (ex: Pendente, Em Andamento, Concluída)
     */
    status: string;
    /**
     * Quantidade de tarefas com este status
     */
    count: number;
};

