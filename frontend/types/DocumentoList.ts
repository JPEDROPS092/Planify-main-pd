/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Tipo0e9Enum } from './Tipo0e9Enum';
/**
 * Serializer simplificado para listagem de documentos
 */
export type DocumentoList = {
    readonly id: number;
    projeto: number;
    readonly projeto_nome: string;
    tarefa?: number | null;
    readonly tarefa_titulo: string;
    titulo: string;
    tipo?: Tipo0e9Enum;
    readonly tipo_display: string;
    versao?: string;
    readonly enviado_por_nome: string;
    readonly data_upload: string;
    /**
     * Tamanho em bytes
     */
    tamanho_arquivo: number;
    /**
     * Tipo MIME do arquivo
     */
    tipo_arquivo: string;
};

