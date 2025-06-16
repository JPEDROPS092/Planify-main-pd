/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Equipe } from '../models/Equipe';
import type { EquipeRequest } from '../models/EquipeRequest';
import type { MembroEquipe } from '../models/MembroEquipe';
import type { MembroEquipeRequest } from '../models/MembroEquipeRequest';
import type { PaginatedEquipeListList } from '../models/PaginatedEquipeListList';
import type { PaginatedMembroEquipeList } from '../models/PaginatedMembroEquipeList';
import type { PaginatedUserMinimalList } from '../models/PaginatedUserMinimalList';
import type { PatchedEquipeRequest } from '../models/PatchedEquipeRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class EquipesService {
    /**
     * Listar equipes
     * Retorna uma lista paginada de equipes.
     * @param minhasEquipes Filtrar apenas minhas equipes
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @param texto Filtrar por nome ou descrição
     * @param usuario Filtrar por membro da equipe
     * @returns PaginatedEquipeListList
     * @throws ApiError
     */
    public static teamsEquipesList(
        minhasEquipes?: boolean,
        ordering?: string,
        page?: number,
        search?: string,
        texto?: string,
        usuario?: number,
    ): CancelablePromise<PaginatedEquipeListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/',
            query: {
                'minhas_equipes': minhasEquipes,
                'ordering': ordering,
                'page': page,
                'search': search,
                'texto': texto,
                'usuario': usuario,
            },
        });
    }
    /**
     * Criar nova equipe
     * Cria uma nova equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static teamsEquipesCreate(
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da equipe
     * Retorna informações detalhadas de uma equipe específica.
     * @param id A unique integer value identifying this Equipe.
     * @returns Equipe
     * @throws ApiError
     */
    public static teamsEquipesRetrieve(
        id: number,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar equipe
     * Atualiza todos os campos de uma equipe existente.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static teamsEquipesUpdate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar equipe parcialmente
     * Atualiza parcialmente uma equipe existente.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static teamsEquipesPartialUpdate(
        id: number,
        requestBody?: PatchedEquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir equipe
     * Remove uma equipe existente.
     * @param id A unique integer value identifying this Equipe.
     * @returns void
     * @throws ApiError
     */
    public static teamsEquipesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Adicionar membro à equipe
     * Adiciona um novo membro à equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public static teamsEquipesAdicionarMembroCreate(
        id: number,
        requestBody: MembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/{id}/adicionar_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar papel do membro
     * Atualiza o papel de um membro na equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public static teamsEquipesAtualizarPapelMembroCreate(
        id: number,
        requestBody: MembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/{id}/atualizar_papel_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar membros da equipe
     * Retorna a lista de membros de uma equipe específica.
     * @param id A unique integer value identifying this Equipe.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedMembroEquipeList
     * @throws ApiError
     */
    public static teamsEquipesMembrosList(
        id: number,
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedMembroEquipeList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/{id}/membros/',
            path: {
                'id': id,
            },
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Remover membro da equipe
     * Remove um membro da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static teamsEquipesRemoverMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/{id}/remover_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retornar usuários disponíveis à equipe
     * Retorna a lista de usuários que podem ser adicionados à equipe.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserMinimalList
     * @throws ApiError
     */
    public static teamsEquipesUsuariosDisponiveisList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserMinimalList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/usuarios_disponiveis/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
}
