/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PapelF38Enum } from './PapelF38Enum';
export type MembroEquipe = {
    readonly id: number;
    equipe: number;
    usuario: number;
    readonly usuario_nome: string;
    readonly usuario_email: string;
    papel: PapelF38Enum;
    readonly papel_display: string;
    readonly adicionado_em: string;
    adicionado_por?: number | null;
    readonly adicionado_por_nome: string;
};

