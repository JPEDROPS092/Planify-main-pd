/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DashboardUsuario } from '../models/DashboardUsuario';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsuRiosService {
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
