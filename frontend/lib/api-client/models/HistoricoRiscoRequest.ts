/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ImpactoEnum } from './ImpactoEnum';
import type { NovaProbabilidadeEnum } from './NovaProbabilidadeEnum';
import type { NovoStatusA52Enum } from './NovoStatusA52Enum';
import type { ProbabilidadeAnteriorEnum } from './ProbabilidadeAnteriorEnum';
export type HistoricoRiscoRequest = {
    risco: number;
    status_anterior: NovoStatusA52Enum;
    novo_status: NovoStatusA52Enum;
    probabilidade_anterior: ProbabilidadeAnteriorEnum;
    nova_probabilidade: NovaProbabilidadeEnum;
    impacto_anterior: ImpactoEnum;
    novo_impacto: ImpactoEnum;
    alterado_por?: number | null;
    observacao?: string | null;
};

