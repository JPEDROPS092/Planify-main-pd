/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ImpactoEnum } from './ImpactoEnum';
import type { NovoStatusA52Enum } from './NovoStatusA52Enum';
import type { ProbabilidadeEnum } from './ProbabilidadeEnum';
export type PatchedRiscoRequest = {
    projeto?: number;
    descricao?: string;
    probabilidade?: ProbabilidadeEnum;
    impacto?: ImpactoEnum;
    status?: NovoStatusA52Enum;
    responsavel_mitigacao?: number | null;
    plano_mitigacao?: string | null;
    plano_contingencia?: string | null;
    criado_por?: number | null;
};

