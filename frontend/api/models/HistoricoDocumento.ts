/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type HistoricoDocumento = {
    readonly id: number;
    documento: number;
    versao_anterior: string;
    arquivo_anterior: string;
    /**
     * Tamanho em bytes
     */
    tamanho_arquivo: number;
    alterado_por?: number | null;
    readonly alterado_por_nome: string;
    readonly data_alteracao: string;
    observacao?: string | null;
};

