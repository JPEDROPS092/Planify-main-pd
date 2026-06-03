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
export type OrcamentoTarefaRequest = {
    tarefa: number;
    valor: string;
    aprovado_por?: number | null;
    observacoes?: string | null;
};

