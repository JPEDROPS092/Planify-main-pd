/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AtribuicaoTarefa } from './AtribuicaoTarefa';
import type { NovoStatus607Enum } from './NovoStatus607Enum';
import type { PrioridadeEnum } from './PrioridadeEnum';
import type { User } from './User';
export type Tarefa = {
    readonly id: number;
    titulo: string;
    descricao: string;
    projeto: number;
    sprint?: number | null;
    data_inicio: string;
    data_termino: string;
    prioridade?: PrioridadeEnum;
    status?: NovoStatus607Enum;
    readonly criado_por: User;
    readonly criado_em: string;
    readonly atualizado_em: string;
    /**
     * Lista de usuários atribuídos a esta tarefa.
     */
    readonly atribuicoes: Array<AtribuicaoTarefa>;
};

