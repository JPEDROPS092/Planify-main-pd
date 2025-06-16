/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Equipe } from '../models/Equipe';
import type { EquipeRequest } from '../models/EquipeRequest';
import type { MembroEquipe } from '../models/MembroEquipe';
import type { PaginatedEquipeListList } from '../models/PaginatedEquipeListList';
import type { PaginatedMembroEquipeList } from '../models/PaginatedMembroEquipeList';
import type { PaginatedPermissaoEquipeList } from '../models/PaginatedPermissaoEquipeList';
import type { PaginatedUserMinimalList } from '../models/PaginatedUserMinimalList';
import type { PatchedEquipeRequest } from '../models/PatchedEquipeRequest';
import type { PatchedPermissaoEquipeRequest } from '../models/PatchedPermissaoEquipeRequest';
import type { PermissaoEquipe } from '../models/PermissaoEquipe';
import type { PermissaoEquipeRequest } from '../models/PermissaoEquipeRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class EquipesService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Listar equipes
     * Retorna uma lista paginada de equipes.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedEquipeListList
     * @throws ApiError
     */
    public apiTeamsEquipesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedEquipeListList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/teams/equipes/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar nova equipe
     * Cria uma novo equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public apiTeamsEquipesCreate(
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return this.httpRequest.request({
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
    public apiTeamsEquipesRetrieve(
        id: number,
    ): CancelablePromise<Equipe> {
        return this.httpRequest.request({
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
    public apiTeamsEquipesUpdate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return this.httpRequest.request({
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
    public apiTeamsEquipesPartialUpdate(
        id: number,
        requestBody?: PatchedEquipeRequest,
    ): CancelablePromise<Equipe> {
        return this.httpRequest.request({
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
    public apiTeamsEquipesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Adicionar membro à equipe
     * Adiciona um membro à equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public apiTeamsEquipesAdicionarMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return this.httpRequest.request({
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
     * Atualizar papel de um membro de equipe
     * Atualiza o papel de um membro da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public apiTeamsEquipesAtualizarPapelMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return this.httpRequest.request({
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
     * Retorna a lista de membros da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedMembroEquipeList
     * @throws ApiError
     */
    public apiTeamsEquipesMembrosList(
        id: number,
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedMembroEquipeList> {
        return this.httpRequest.request({
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
     * Remover membro de equipe
     * Remove um membro da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public apiTeamsEquipesRemoverMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
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
     * Retorna a lista de usuários disponíveis para adicionar a uma equipe.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserMinimalList
     * @throws ApiError
     */
    public apiTeamsEquipesUsuariosDisponiveisList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserMinimalList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/teams/equipes/usuarios_disponiveis/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Listar permissões de equipe
     * Retorna uma lista paginada de permissões de equipe.
     * @param equipe
     * @param modulo * `TAREFAS` - Tarefas
     * * `SPRINTS` - Sprints
     * * `DOCUMENTOS` - Documentos
     * * `RISCOS` - Riscos
     * * `CUSTOS` - Custos
     * @param page A page number within the paginated result set.
     * @param papel * `PO` - Product Owner
     * * `SM` - Scrum Master
     * * `DEV` - Desenvolvedor
     * * `QA` - Analista de Qualidade
     * * `DESIGN` - Designer
     * * `ANALISTA` - Analista
     * @param permissao * `VISUALIZAR` - Visualizar
     * * `CRIAR` - Criar
     * * `EDITAR` - Editar
     * * `EXCLUIR` - Excluir
     * @returns PaginatedPermissaoEquipeList
     * @throws ApiError
     */
    public apiTeamsPermissoesList(
        equipe?: number,
        modulo?: 'CUSTOS' | 'DOCUMENTOS' | 'RISCOS' | 'SPRINTS' | 'TAREFAS',
        page?: number,
        papel?: 'ANALISTA' | 'DESIGN' | 'DEV' | 'PO' | 'QA' | 'SM',
        permissao?: 'CRIAR' | 'EDITAR' | 'EXCLUIR' | 'VISUALIZAR',
    ): CancelablePromise<PaginatedPermissaoEquipeList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/teams/permissoes/',
            query: {
                'equipe': equipe,
                'modulo': modulo,
                'page': page,
                'papel': papel,
                'permissao': permissao,
            },
        });
    }
    /**
     * Criar nova permissão de equipe
     * Cria uma novo permissão de equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public apiTeamsPermissoesCreate(
        requestBody: PermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/teams/permissoes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da permissão de equipe
     * Retorna informações detalhadas de uma permissão de equipe específica.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public apiTeamsPermissoesRetrieve(
        id: number,
    ): CancelablePromise<PermissaoEquipe> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar permissão de equipe
     * Atualiza todos os campos de uma permissão de equipe existente.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public apiTeamsPermissoesUpdate(
        id: number,
        requestBody: PermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return this.httpRequest.request({
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
     * Atualizar permissão de equipe parcialmente
     * Atualiza parcialmente uma permissão de equipe existente.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public apiTeamsPermissoesPartialUpdate(
        id: number,
        requestBody?: PatchedPermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return this.httpRequest.request({
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
     * Excluir permissão de equipe
     * Remove uma permissão de equipe existente.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @returns void
     * @throws ApiError
     */
    public apiTeamsPermissoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
