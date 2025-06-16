/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ModuloEnum } from './ModuloEnum';
import type { PapelF38Enum } from './PapelF38Enum';
import type { PermissaoEnum } from './PermissaoEnum';
export type PermissaoEquipe = {
    readonly id: number;
    papel: PapelF38Enum;
    readonly papel_display: string;
    equipe: number;
    modulo: ModuloEnum;
    readonly modulo_display: string;
    permissao: PermissaoEnum;
    readonly permissao_display: string;
};

