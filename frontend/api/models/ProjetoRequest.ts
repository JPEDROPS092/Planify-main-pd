/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PrioridadeEnum } from './PrioridadeEnum';
import type { Status18dEnum } from './Status18dEnum';
/**
 * Serializer completo para projetos.
 *
 * Inclui informações detalhadas do projeto, membros, estatísticas de sprints e tarefas.
 */
export type ProjetoRequest = {
    titulo: string;
    descricao: string;
    data_inicio: string;
    data_fim: string;
    status?: Status18dEnum;
    prioridade?: PrioridadeEnum;
    arquivado?: boolean;
};

