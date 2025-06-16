/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AtribuicaoTarefa } from './AtribuicaoTarefa';
import type { NovoStatus607Enum } from './NovoStatus607Enum';
import type { PrioridadeEnum } from './PrioridadeEnum';
import type { User } from './User';
export type TarefaList = {
    readonly id: number;
    titulo: string;
    projeto: number;
    sprint?: number | null;
    status?: NovoStatus607Enum;
    prioridade?: PrioridadeEnum;
    data_termino: string;
    readonly criado_por: User;
    /**
     * Lista de usuários atribuídos a esta tarefa.
     */
    readonly atribuicoes: Array<AtribuicaoTarefa>;
};

