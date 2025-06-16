/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedUserProfileList } from '../models/PaginatedUserProfileList';
import type { PatchedUserProfileRequest } from '../models/PatchedUserProfileRequest';
import type { UserProfile } from '../models/UserProfile';
import type { UserProfileRequest } from '../models/UserProfileRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PerfisService {
    /**
     * Listar perfis
     * Retorna uma lista paginada de perfis.
     * @param page A page number within the paginated result set.
     * @returns PaginatedUserProfileList
     * @throws ApiError
     */
    public static authProfilesList(
        page?: number,
    ): CancelablePromise<PaginatedUserProfileList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/profiles/',
            query: {
                'page': page,
            },
        });
    }
    /**
     * Criar novo perfil
     * Cria um novo perfil.
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static authProfilesCreate(
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do perfil
     * Retorna informações detalhadas de um perfil específico.
     * @param id A unique integer value identifying this user profile.
     * @returns UserProfile
     * @throws ApiError
     */
    public static authProfilesRetrieve(
        id: number,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar perfil
     * Atualiza todos os campos de um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static authProfilesUpdate(
        id: number,
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar perfil parcialmente
     * Atualiza parcialmente um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static authProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedUserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir perfil
     * Remove um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @returns void
     * @throws ApiError
     */
    public static authProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
