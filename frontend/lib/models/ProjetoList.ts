/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PrioridadeEnum } from './PrioridadeEnum';
import type { Status18dEnum } from './Status18dEnum';
/**
 * Serializer otimizado para listagem de projetos.
 *
 * Inclui informações resumidas e estatísticas básicas para listagem eficiente.
 */
export type ProjetoList = {
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
    readonly criado_em: string;
    readonly atualizado_em: string;
    arquivado?: boolean;
    /**
     * Número total de membros neste projeto
     */
    readonly membros_count: number;
    /**
     * Número total de tarefas neste projeto
     */
    readonly tasks_count: number;
    /**
     * Progresso do projeto em percentual (0-100)
     */
    readonly progresso: number;
    /**
     * Nome de usuário do criador
     */
    readonly criador_username: string;
    /**
     * Indica se o projeto está atrasado
     */
    readonly atrasado: boolean;
};

