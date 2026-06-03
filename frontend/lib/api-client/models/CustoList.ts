/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Serializer simplificado para listagem de custos.
 *
 * Projetado para exibir uma visão concisa dos custos, ideal para listas
 * ou tabelas onde nem todos os detalhes do Custo são necessários.
 * Inclui campos de leitura para nomes relacionados e o valor 'display' do tipo.
 */
export type CustoList = {
    readonly id: number;
    projeto: number;
    readonly projeto_nome: string;
    tarefa?: number | null;
    readonly tarefa_titulo: string;
    readonly categoria_nome: string;
    descricao: string;
    valor: string;
    readonly tipo_display: string;
    data: string;
};

