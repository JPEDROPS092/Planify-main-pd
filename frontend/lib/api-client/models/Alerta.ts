/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AlertaStatusEnum } from './AlertaStatusEnum';
import type { AlertaTipoEnum } from './AlertaTipoEnum';
/**
 * Serializer para o modelo Alerta.
 *
 * Inclui todos os campos do modelo Alerta.
 * Adiciona campos de leitura para exibir o valor textual dos campos de escolha
 * ('tipo', 'status') e nomes relacionados (projeto, tarefa, resolvedor).
 */
export type Alerta = {
    readonly id: number;
    tipo: AlertaTipoEnum;
    readonly tipo_display: string;
    projeto: number;
    readonly projeto_nome: string;
    tarefa?: number | null;
    readonly tarefa_titulo: string;
    percentual: string;
    mensagem: string;
    status?: AlertaStatusEnum;
    readonly status_display: string;
    readonly data_criacao: string;
    readonly data_resolucao: string | null;
    resolvido_por?: number | null;
    readonly resolvido_por_nome: string;
};

