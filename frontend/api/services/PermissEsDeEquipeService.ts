/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedPermissaoEquipeList } from '../models/PaginatedPermissaoEquipeList';
import type { PatchedPermissaoEquipeRequest } from '../models/PatchedPermissaoEquipeRequest';
import type { PermissaoEquipe } from '../models/PermissaoEquipe';
import type { PermissaoEquipeRequest } from '../models/PermissaoEquipeRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PermissEsDeEquipeService {
    /**
     * Listar permissões de equipe
     * Retorna uma lista de permissões de equipe.
     * @param page A page number within the paginated result set.
     * @returns PaginatedPermissaoEquipeList
     * @throws ApiError
     */
    public static teamsPermissoesList(
        page?: number,
    ): CancelablePromise<PaginatedPermissaoEquipeList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/permissoes/',
            query: {
                'page': page,
            },
        });
    }
    /**
     * Criar permissão
     * Cria uma nova permissão de equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static teamsPermissoesCreate(
        requestBody: PermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/permissoes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da permissão
     * Retorna detalhes de uma permissão específica.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static teamsPermissoesRetrieve(
        id: number,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar permissão
     * Atualiza uma permissão de equipe existente.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static teamsPermissoesUpdate(
        id: number,
        requestBody: PermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar permissão parcialmente
     * Atualiza parcialmente uma permissão de equipe.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static teamsPermissoesPartialUpdate(
        id: number,
        requestBody?: PatchedPermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir permissão
     * Remove uma permissão de equipe.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @returns void
     * @throws ApiError
     */
    public static teamsPermissoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
