/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { NovoStatus607Enum } from './NovoStatus607Enum';
import type { PrioridadeEnum } from './PrioridadeEnum';
export type PatchedTarefaRequest = {
    titulo?: string;
    descricao?: string;
    projeto?: number;
    sprint?: number | null;
    data_inicio?: string;
    data_termino?: string;
    prioridade?: PrioridadeEnum;
    status?: NovoStatus607Enum;
};

