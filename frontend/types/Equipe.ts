/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MembroEquipe } from './MembroEquipe';
import type { PermissaoEquipe } from './PermissaoEquipe';
export type Equipe = {
    readonly id: number;
    nome: string;
    descricao?: string | null;
    criado_por?: number | null;
    /**
     * Nome completo do usuário que criou a equipe.
     */
    readonly criado_por_nome: string;
    readonly criado_em: string;
    readonly atualizado_em: string;
    /**
     * Lista de membros desta equipe.
     */
    readonly membros: Array<MembroEquipe>;
    /**
     * Lista de permissões associadas a esta equipe.
     */
    readonly permissoes: Array<PermissaoEquipe>;
    /**
     * Número total de membros nesta equipe.
     */
    readonly total_membros: number;
};

