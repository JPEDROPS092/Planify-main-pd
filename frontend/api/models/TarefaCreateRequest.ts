/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PrioridadeEnum } from './PrioridadeEnum';
import type { TarefaCreateStatusEnum } from './TarefaCreateStatusEnum';
export type TarefaCreateRequest = {
    /**
     * Título da tarefa
     */
    titulo: string;
    /**
     * Descrição da tarefa
     */
    descricao?: string | null;
    /**
     * Data de início da tarefa
     */
    data_inicio: string;
    /**
     * Data de término prevista da tarefa
     */
    data_fim: string;
    /**
     * Prioridade da tarefa
     *
     * * `BAIXA` - BAIXA
     * * `MEDIA` - MEDIA
     * * `ALTA` - ALTA
     */
    prioridade: PrioridadeEnum;
    /**
     * Status inicial da tarefa
     *
     * * `PENDENTE` - PENDENTE
     * * `EM_ANDAMENTO` - EM_ANDAMENTO
     * * `CONCLUIDA` - CONCLUIDA
     * * `BLOQUEADA` - BLOQUEADA
     */
    status: TarefaCreateStatusEnum;
    /**
     * IDs dos usuários responsáveis pela tarefa
     */
    responsaveis?: Array<number>;
};

