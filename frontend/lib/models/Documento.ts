/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Comentario } from './Comentario';
import type { HistoricoDocumento } from './HistoricoDocumento';
import type { Tipo0e9Enum } from './Tipo0e9Enum';
export type Documento = {
    readonly id: number;
    projeto: number;
    readonly projeto_nome: string;
    tarefa?: number | null;
    readonly tarefa_titulo: string;
    titulo: string;
    descricao?: string | null;
    tipo?: Tipo0e9Enum;
    readonly tipo_display: string;
    arquivo: string;
    /**
     * Tamanho em bytes
     */
    readonly tamanho_arquivo: number;
    /**
     * Tipo MIME do arquivo
     */
    readonly tipo_arquivo: string;
    versao?: string;
    enviado_por?: number | null;
    readonly enviado_por_nome: string;
    readonly data_upload: string;
    readonly atualizado_em: string;
    readonly comentarios: Array<Comentario>;
    readonly historico: Array<HistoricoDocumento>;
};

