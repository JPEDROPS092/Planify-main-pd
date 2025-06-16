/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColunaKanban } from './ColunaKanban';
export type KanbanResponse = {
    /**
     * ID do projeto
     */
    projeto: number;
    /**
     * Título do projeto
     */
    titulo: string;
    /**
     * Colunas do quadro Kanban
     */
    colunas: Array<ColunaKanban>;
};

