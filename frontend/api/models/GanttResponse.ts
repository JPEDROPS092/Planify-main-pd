/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TarefaGantt } from './TarefaGantt';
export type GanttResponse = {
    /**
     * ID do projeto
     */
    projeto: number;
    /**
     * Título do projeto
     */
    titulo: string;
    /**
     * Tarefas do projeto para visualização Gantt
     */
    tarefas: Array<TarefaGantt>;
};

