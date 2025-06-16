/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer para o modelo OrcamentoTarefa.
 *
 * Inclui campos para o orçamento de uma tarefa específica e informações de aprovação.
 * Adiciona campos de leitura para nomes relacionados (aprovador, tarefa, projeto da tarefa)
 * e campos calculados (valor utilizado, valor restante, percentual utilizado).
 */
export type OrcamentoTarefa = {
    readonly id: number;
    tarefa: number;
    readonly tarefa_titulo: string;
    readonly projeto_nome: string;
    valor: string;
    readonly data_aprovacao: string;
    aprovado_por?: number | null;
    readonly aprovado_por_nome: string;
    observacoes?: string | null;
    readonly valor_utilizado: string;
    readonly valor_restante: string;
    readonly percentual_utilizado: string;
};

