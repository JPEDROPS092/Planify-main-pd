/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MembroProjetoPapelEnum } from './MembroProjetoPapelEnum';
/**
 * Serializer para membros de projeto.
 *
 * Inclui informações básicas do usuário e seu papel no projeto.
 */
export type MembroProjeto = {
    readonly id: number;
    readonly usuario_id: number;
    readonly username: string;
    readonly full_name: string;
    papel: MembroProjetoPapelEnum;
    /**
     * Nome do papel para exibição
     */
    readonly papel_display: string;
};

