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
export type CustoRequest = {
    projeto: number;
    tarefa?: number | null;
    categoria?: number | null;
    descricao: string;
    valor: string;
    tipo?: CustoTipoEnum;
    data: string;
    comprovante?: Blob | null;
    observacoes?: string | null;
    criado_por?: number | null;
};

