/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColunaKanbanRequest } from './ColunaKanbanRequest';
export type PatchedKanbanResponseRequest = {
    /**
     * ID do projeto
     */
    projeto?: number;
    /**
     * Título do projeto
     */
    titulo?: string;
    /**
     * Colunas do quadro Kanban
     */
    colunas?: Array<ColunaKanbanRequest>;
};

