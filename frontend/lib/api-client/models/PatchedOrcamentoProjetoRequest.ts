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
export type PatchedOrcamentoProjetoRequest = {
    projeto?: number;
    valor_total?: string;
    aprovado_por?: number | null;
    observacoes?: string | null;
};

