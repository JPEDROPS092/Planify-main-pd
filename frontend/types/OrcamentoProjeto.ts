/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer para o modelo OrcamentoProjeto.
 *
 * Inclui campos para o orçamento total e informações de aprovação.
 * Adiciona campos de leitura para nomes relacionados (aprovador, projeto)
 * e campos calculados (valor utilizado, valor restante, percentual utilizado).
 */
export type OrcamentoProjeto = {
    readonly id: number;
    projeto: number;
    readonly projeto_nome: string;
    valor_total: string;
    readonly data_aprovacao: string;
    aprovado_por?: number | null;
    readonly aprovado_por_nome: string;
    observacoes?: string | null;
    readonly valor_utilizado: string;
    readonly valor_restante: string;
    readonly percentual_utilizado: string;
};

