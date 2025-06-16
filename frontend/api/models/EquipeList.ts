/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer simplificado para listagem de equipes
 */
export type EquipeList = {
    readonly id: number;
    nome: string;
    /**
     * Nome completo do criador da equipe.
     */
    readonly criado_por_nome: string;
    readonly criado_em: string;
    /**
     * Número total de membros nesta equipe.
     */
    readonly total_membros: number;
};

