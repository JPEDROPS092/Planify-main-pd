/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { LoginRequestRequest } from '../models/LoginRequestRequest';
import type { LoginResponse } from '../models/LoginResponse';
import type { LogoutResponse } from '../models/LogoutResponse';
import type { RefreshRequestRequest } from '../models/RefreshRequestRequest';
import type { RefreshResponse } from '../models/RefreshResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AutenticaOService {
    /**
     * Login de usuário
     *
     * Realiza o login do usuário e retorna os tokens de acesso e refresh.
     *
     * O token de acesso deve ser usado no header de todas as requisições:
     * `Authorization: JWT <access_token>`
     *
     * Quando o token de acesso expirar (após 1 hora), use o token de refresh para obter um novo.
     *
     * @param requestBody
     * @returns LoginResponse
     * @throws ApiError
     */
    public static authLoginCreate(
        requestBody: LoginRequestRequest,
    ): CancelablePromise<LoginResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/login/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                401: `Credenciais inválidas`,
            },
        });
    }
    /**
     * Logout de usuário
     * Realiza o logout do usuário invalidando o token atual.
     * @returns LogoutResponse
     * @throws ApiError
     */
    public static authLogoutCreate(): CancelablePromise<LogoutResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/logout/',
        });
    }
    /**
     * Atualizar token de acesso
     *
     * Atualiza um token de acesso expirado usando o token de refresh.
     *
     * @param requestBody
     * @returns RefreshResponse
     * @throws ApiError
     */
    public static authTokenRefreshCreate(
        requestBody: RefreshRequestRequest,
    ): CancelablePromise<RefreshResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/token/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
