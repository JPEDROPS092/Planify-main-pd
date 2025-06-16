/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ComentarioTarefa } from '../models/ComentarioTarefa';
import type { ComentarioTarefaRequest } from '../models/ComentarioTarefaRequest';
import type { PaginatedComentarioTarefaList } from '../models/PaginatedComentarioTarefaList';
import type { PatchedComentarioTarefaRequest } from '../models/PatchedComentarioTarefaRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ComentRiosDeTarefasService {
    /**
     * Listar comentários de tarefas
     * Retorna uma lista de comentários de tarefas.
     * @param autor Filtrar por ID do autor
     * @param ordering Ordenar resultados (ex: -criado_em)
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @param tarefa Filtrar por ID da tarefa
     * @returns PaginatedComentarioTarefaList
     * @throws ApiError
     */
    public static tasksComentariosList(
        autor?: number,
        ordering?: string,
        page?: number,
        search?: string,
        tarefa?: number,
    ): CancelablePromise<PaginatedComentarioTarefaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/comentarios/',
            query: {
                'autor': autor,
                'ordering': ordering,
                'page': page,
                'search': search,
                'tarefa': tarefa,
            },
        });
    }
    /**
     * Criar comentário
     * Adiciona um novo comentário a uma tarefa.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public static tasksComentariosCreate(
        requestBody: ComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/comentarios/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes de comentário
     * Retorna informações detalhadas de um comentário específico.
     * @param id A unique integer value identifying this Comentário.
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public static tasksComentariosRetrieve(
        id: number,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar comentário
     * Atualiza o texto de um comentário existente.
     * @param id A unique integer value identifying this Comentário.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public static tasksComentariosUpdate(
        id: number,
        requestBody: ComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar comentário parcialmente
     * Atualiza parcialmente o texto de um comentário existente.
     * @param id A unique integer value identifying this Comentário.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public static tasksComentariosPartialUpdate(
        id: number,
        requestBody?: PatchedComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir comentário
     * Remove permanentemente um comentário.
     * @param id A unique integer value identifying this Comentário.
     * @returns void
     * @throws ApiError
     */
    public static tasksComentariosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
