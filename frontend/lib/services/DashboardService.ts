/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DashboardUsuario } from '../models/DashboardUsuario';
import type { MetricasProjeto } from '../models/MetricasProjeto';
import type { VisaoGeralDashboard } from '../models/VisaoGeralDashboard';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DashboardService {
    /**
     * Visão Geral do Dashboard
     * Retorna uma visão geral do sistema, incluindo o número total de projetos, tarefas e a distribuição de tarefas por status. Requer autenticação.
     * @returns VisaoGeralDashboard Dados consolidados do dashboard.
     * @throws ApiError
     */
    public static visaoGeralDashboardRetrieve(): CancelablePromise<VisaoGeralDashboard> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/dashboard/',
        });
    }
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
    /**
     * Dashboard Pessoal do Usuário
     * Retorna dados personalizados para o dashboard do usuário autenticado, incluindo projetos gerenciados, suas tarefas por status, tarefas atrasadas e próximas tarefas. Requer autenticação.
     * @returns DashboardUsuario Dados consolidados para o dashboard do usuário.
     * @throws ApiError
     */
    public static dashboardUsuarioRetrieve(): CancelablePromise<DashboardUsuario> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/user/dashboard/',
        });
    }
}
