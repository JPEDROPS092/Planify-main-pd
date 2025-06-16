/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedPermissionList } from '../models/PaginatedPermissionList';
import type { PatchedPermissionRequest } from '../models/PatchedPermissionRequest';
import type { Permission } from '../models/Permission';
import type { PermissionRequest } from '../models/PermissionRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PermissEsService {
    /**
     * Listar permissões
     * Retorna uma lista paginada de permissões.
     * @param page A page number within the paginated result set.
     * @returns PaginatedPermissionList
     * @throws ApiError
     */
    public static authPermissionsList(
        page?: number,
    ): CancelablePromise<PaginatedPermissionList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/permissions/',
            query: {
                'page': page,
            },
        });
    }
    /**
     * Criar nova permissão
     * Cria uma nova permissão.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static authPermissionsCreate(
        requestBody: PermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/permissions/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da permissão
     * Retorna informações detalhadas de uma permissão específica.
     * @param id A unique integer value identifying this permission.
     * @returns Permission
     * @throws ApiError
     */
    public static authPermissionsRetrieve(
        id: number,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar permissão
     * Atualiza todos os campos de uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static authPermissionsUpdate(
        id: number,
        requestBody: PermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar permissão parcialmente
     * Atualiza parcialmente uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static authPermissionsPartialUpdate(
        id: number,
        requestBody?: PatchedPermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir permissão
     * Remove uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @returns void
     * @throws ApiError
     */
    public static authPermissionsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
