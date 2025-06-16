/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChangePasswordRequest } from '../models/ChangePasswordRequest';
import type { User } from '../models/User';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PerfilService {
    /**
     * Alterar senha
     * Altera a senha do usuário autenticado.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersChangePasswordCreate(
        requestBody: ChangePasswordRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/change-password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Alterar senha
     * Altera a senha do usuário autenticado.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersChangePasswordCreate2(
        requestBody: ChangePasswordRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/change_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retornar minhas informações
     * Retorna as informações do usuário autenticado.
     * @returns User
     * @throws ApiError
     */
    public static authUsersMeRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/users/me/',
        });
    }
    /**
     * Retornar minhas permissões
     * Retorna as permissões do usuário autenticado.
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersPermissionsRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/users/permissions/',
        });
    }
}
