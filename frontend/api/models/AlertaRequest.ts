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
export type AlertaRequest = {
    tipo: AlertaTipoEnum;
    projeto: number;
    tarefa?: number | null;
    percentual: string;
    mensagem: string;
    status?: AlertaStatusEnum;
    resolvido_por?: number | null;
};

