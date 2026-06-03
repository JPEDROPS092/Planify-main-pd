/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type HistoricoDocumentoRequest = {
    documento: number;
    versao_anterior: string;
    arquivo_anterior: Blob;
    /**
     * Tamanho em bytes
     */
    tamanho_arquivo: number;
    alterado_por?: number | null;
    observacao?: string | null;
};

