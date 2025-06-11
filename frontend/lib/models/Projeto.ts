/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MembroProjeto } from './MembroProjeto';
import type { PrioridadeEnum } from './PrioridadeEnum';
import type { Status18dEnum } from './Status18dEnum';
/**
 * Serializer completo para projetos.
 *
 * Inclui informações detalhadas do projeto, membros, estatísticas de sprints e tarefas.
 */
export type Projeto = {
    readonly id: number;
    titulo: string;
    descricao: string;
    data_inicio: string;
    data_fim: string;
    status?: Status18dEnum;
    /**
     * Nome do status para exibição
     */
    readonly status_display: string;
    prioridade?: PrioridadeEnum;
    /**
     * Nome da prioridade para exibição
     */
    readonly prioridade_display: string;
    readonly criado_por: number | null;
    /**
     * Nome de usuário do criador
     */
    readonly criador_username: string;
    /**
     * Nome completo do criador
     */
    readonly criador_nome: string;
    readonly criado_em: string;
    readonly atualizado_em: string;
    arquivado?: boolean;
    /**
     * Lista de membros associados ao projeto
     */
    readonly membros: Array<MembroProjeto>;
    /**
     * Número total de sprints neste projeto
     */
    readonly sprints_count: number;
    /**
     * Número total de tarefas neste projeto
     */
    readonly tasks_count: number;
    /**
     * Progresso do projeto em percentual (0-100)
     */
    readonly progresso: number;
    /**
     * Dias restantes até a data de fim
     */
    readonly dias_restantes: number;
    /**
     * Indica se o projeto está atrasado
     */
    readonly atrasado: boolean;
};

