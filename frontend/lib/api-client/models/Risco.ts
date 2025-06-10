/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HistoricoRisco } from './HistoricoRisco';
import type { ImpactoEnum } from './ImpactoEnum';
import type { NovoStatusA52Enum } from './NovoStatusA52Enum';
import type { ProbabilidadeEnum } from './ProbabilidadeEnum';
export type Risco = {
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
    plano_mitigacao?: string | null;
    plano_contingencia?: string | null;
    readonly data_identificacao: string;
    criado_por?: number | null;
    readonly criado_por_nome: string;
    readonly atualizado_em: string;
    readonly nivel_risco: string;
    readonly historico: Array<HistoricoRisco>;
};

