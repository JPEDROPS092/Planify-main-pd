/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CustoTipoEnum } from './CustoTipoEnum';
/**
 * Serializer detalhado para o modelo Custo.
 *
 * Inclui todos os campos do modelo Custo e adiciona campos de leitura
 * para exibir nomes relacionados de outros modelos (usuário, projeto, tarefa, categoria)
 * e o valor textual dos campos de escolha ('tipo').
 */
export type Custo = {
    readonly id: number;
    projeto: number;
    readonly projeto_nome: string;
    tarefa?: number | null;
    readonly tarefa_titulo: string;
    categoria?: number | null;
    readonly categoria_nome: string;
    descricao: string;
    valor: string;
    tipo?: CustoTipoEnum;
    readonly tipo_display: string;
    data: string;
    comprovante?: string | null;
    observacoes?: string | null;
    criado_por?: number | null;
    readonly criado_por_nome: string;
    readonly criado_em: string;
    readonly atualizado_em: string;
};

