/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { NovoStatus607Enum } from './NovoStatus607Enum';
export type HistoricoStatusTarefa = {
    readonly id: number;
    tarefa: number;
    status_anterior: NovoStatus607Enum;
    readonly status_anterior_display: string;
    novo_status: NovoStatus607Enum;
    readonly novo_status_display: string;
    alterado_por?: number | null;
    readonly alterado_por_nome: string;
    readonly alterado_em: string;
};

