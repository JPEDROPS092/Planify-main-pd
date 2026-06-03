/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Tipo0e9Enum } from './Tipo0e9Enum';
export type PatchedDocumentoRequest = {
    projeto?: number;
    tarefa?: number | null;
    titulo?: string;
    descricao?: string | null;
    tipo?: Tipo0e9Enum;
    arquivo?: Blob;
    versao?: string;
    enviado_por?: number | null;
};

