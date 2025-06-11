/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ImpactoEnum } from './ImpactoEnum';
import type { NovoStatusA52Enum } from './NovoStatusA52Enum';
import type { ProbabilidadeEnum } from './ProbabilidadeEnum';
/**
 * Serializer simplificado para listagem de riscos
 */
export type RiscoList = {
    readonly id: number;
    projeto: number;
    readonly projeto_nome: string;
    descricao: string;
    probabilidade: ProbabilidadeEnum;
    readonly probabilidade_display: string;
    impacto: ImpactoEnum;
    readonly impacto_display: string;
    status?: NovoStatusA52Enum;
    readonly status_display: string;
    responsavel_mitigacao?: number | null;
    readonly responsavel_mitigacao_nome: string;
    readonly data_identificacao: string;
    readonly nivel_risco: string;
};

