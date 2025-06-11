/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MetricasProjeto } from '../models/MetricasProjeto';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ProjetosService {
    /**
     * Métricas Detalhadas do Projeto
     * Fornece métricas detalhadas para um projeto específico, como distribuição de tarefas por status, progresso, riscos ativos, custos e dias restantes. Acessível publicamente para fins de demonstração ou integração externa.
     * @param idProjeto ID numérico do projeto para o qual as métricas são solicitadas.
     * @returns MetricasProjeto Métricas detalhadas do projeto.
     * @throws ApiError
     */
    public static metricasProjetoRetrieve(
        idProjeto: number,
    ): CancelablePromise<MetricasProjeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id_projeto}/metrics/',
            path: {
                'id_projeto': idProjeto,
            },
            errors: {
                404: `O projeto com o ID especificado não foi encontrado.`,
            },
        });
    }
}
