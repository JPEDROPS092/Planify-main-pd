/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ImpactoEnum } from './ImpactoEnum';
import type { NovaProbabilidadeEnum } from './NovaProbabilidadeEnum';
import type { NovoStatusA52Enum } from './NovoStatusA52Enum';
import type { ProbabilidadeAnteriorEnum } from './ProbabilidadeAnteriorEnum';
export type HistoricoRisco = {
    readonly id: number;
    risco: number;
    status_anterior: NovoStatusA52Enum;
    readonly status_anterior_display: string;
    novo_status: NovoStatusA52Enum;
    readonly novo_status_display: string;
    probabilidade_anterior: ProbabilidadeAnteriorEnum;
    readonly probabilidade_anterior_display: string;
    nova_probabilidade: NovaProbabilidadeEnum;
    readonly nova_probabilidade_display: string;
    impacto_anterior: ImpactoEnum;
    readonly impacto_anterior_display: string;
    novo_impacto: ImpactoEnum;
    readonly novo_impacto_display: string;
    alterado_por?: number | null;
    readonly alterado_por_nome: string;
    readonly alterado_em: string;
    observacao?: string | null;
};

